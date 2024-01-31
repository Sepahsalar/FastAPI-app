from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, field_validator

def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, order_time):
	small_order_surcharge = max(0, 10 - (cart_value / 100))
	base_delivery_fee = 2
	additional_distance_fee = max(1, ((delivery_distance - 1000) // 500) + 1)
	bulk_surcharge = max(0, (number_of_items - 4) * 0.5)

	if number_of_items > 12:
		bulk_fee = 1.20
	else:
		bulk_fee = 0
  
	total_surcharge = small_order_surcharge + bulk_surcharge + bulk_fee
	total_delivery_fee = base_delivery_fee + additional_distance_fee + total_surcharge
	total_delivery_fee = min(15, total_delivery_fee)

	if cart_value >= 20000:
		total_delivery_fee = 0

	if is_friday_rush(order_time):
		total_delivery_fee *= 1.2
		total_delivery_fee = min(15, total_delivery_fee)

	return round(total_delivery_fee * 100)

def is_friday_rush(order_time):
	delivery_day = order_time.weekday()
	delivery_time_utc = order_time.time()
	friday_rush_start = datetime.strptime('15:00', '%H:%M').time()
	friday_rush_end = datetime.strptime('19:00', '%H:%M').time() 
	return delivery_day == 4 and friday_rush_start <= delivery_time_utc <= friday_rush_end

app = FastAPI()
class CartItems(BaseModel):
	cart_value: conint(gt=0)
	delivery_distance: conint(gt=0)
	number_of_items: conint(gt=0)
	time: str

	@field_validator("time")
	def validate_time_format(cls, value):
		try:
			datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
		except ValueError:
			raise ValueError("Invalid 'time' format. Use ISO format: YYYY-MM-DDTHH:MM:SSZ")
		return value

@app.post("/calculate_delivery_fee")
async def calculate_delivery_fee_api(cart_items: CartItems):
	try:
		order_time = datetime.strptime(cart_items.time, '%Y-%m-%dT%H:%M:%SZ')
	except ValueError:
		raise HTTPException(status_code=400, detail="Invalid 'time' format. Use ISO format: YYYY-MM-DDTHH:MM:SSZ")

	try:
		delivery_fee = calculate_delivery_fee(cart_items.cart_value, cart_items.delivery_distance, cart_items.number_of_items, order_time)
		response = {'delivery_fee': delivery_fee}
		return response
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
