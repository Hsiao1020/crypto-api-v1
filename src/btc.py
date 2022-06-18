from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from flasgger import swag_from

from src.database import db, BTC, BTCSchema
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

btc = Blueprint("btc", __name__, url_prefix="/api/v1/btc")

btc_schema = BTCSchema()
btcs_schema = BTCSchema(many=True)


@btc.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_btc():
    if request.method == "POST":
        btc_datetime = request.get_json().get("datetime", None)
        btc_datetime = datetime.fromisoformat(btc_datetime[:-1] + '+00:00')
        Open = request.get_json().get("Open", None)
        High = request.get_json().get("High", None)
        Low = request.get_json().get("Low", None)
        Close = request.get_json().get("Close", None)
        Adj_Close = request.get_json().get("Adj Close", None)
        Volume = request.get_json().get("Volume", None)

        btc_price = BTC(
            btc_datetime=btc_datetime,
            Open=Open,
            High=High,
            Low=Low,
            Close=Close,
            Adj_Close=Adj_Close,
            Volume=Volume
        )

        db.session.add(btc_price)
        db.session.commit()
        return btc_schema.jsonify(btc_price), HTTP_201_CREATED

    else:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
    
        all_btc_price = BTC.query.paginate(page=page, per_page=per_page)

        result = btcs_schema.dump(all_btc_price.items)
        return jsonify(result), HTTP_200_OK

        # input example
        # {
        #     "datetime": "2020-07-01+08:00:00",
        #     "Open": 31699.585938,
        #     "High": 31831.242188,
        #     "Low": 31661.035156,
        #     "Close": 31719.363281,
        #     "Adj Close": 31719.363281,
        #     "Volume": 855289856
        # }


@btc.get("/<string:btc_datetime>")
@jwt_required()
def get_btc_price(btc_datetime):
    try:
        btc_datetime = datetime.strptime(btc_datetime, "%Y-%m-%d+%H:%M:%S")
    except ValueError:
        return jsonify({"message": "Incorrect argument format, datetime should be yyyy-MM-dd+HH:mm:ss"})

    btc_price = BTC.query.filter_by(btc_datetime=btc_datetime).first()

    if not btc_price:
        return jsonify({"message": f"BTC price not found at {btc_datetime}"}), HTTP_404_NOT_FOUND

    return btc_schema.jsonify(btc_price), HTTP_200_OK


@btc.put("/<string:btc_datetime>")
@btc.patch("/<string:btc_datetime>")
@jwt_required()
def edit_btc_price(btc_datetime):
    try:
        btc_datetime = datetime.strptime(btc_datetime, "%Y-%m-%d+%H:%M:%S")
    except ValueError:
        return jsonify({"message": "Incorrect argument format, datetime should be yyyy-MM-dd+HH:mm:ss"})

    btc_price = BTC.query.filter_by(btc_datetime=btc_datetime).first()

    if not btc_price:
        return jsonify({"message": f"BTC price not found at {btc_datetime}"}), HTTP_404_NOT_FOUND

    Open = request.get_json().get("Open", None)
    High = request.get_json().get("High", None)
    Low = request.get_json().get("Low", None)
    Close = request.get_json().get("Close", None)
    Adj_Close = request.get_json().get("Adj Close", None)
    Volume = request.get_json().get("Volume", None)

    btc_price.Open = Open
    btc_price.High = High
    btc_price.Low = Low
    btc_price.Close = Close
    btc_price.Adj_Close = Adj_Close
    btc_price.Volume = Volume

    db.session.commit()
    return btc_schema.jsonify(btc_price), HTTP_200_OK


@btc.delete("/<string:btc_datetime>")
@jwt_required()
def delete_btc_price(btc_datetime):
    try:
        btc_datetime = datetime.strptime(btc_datetime, "%Y-%m-%d+%H:%M:%S")
    except ValueError:
        return jsonify({"message": "Incorrect argument format, datetime should be yyyy-MM-dd+HH:mm:ss"})

    btc_price = BTC.query.filter_by(btc_datetime=btc_datetime).first()

    if not btc_price:
        return jsonify({"message": f"BTC price not found at {btc_datetime}"}), HTTP_404_NOT_FOUND

    db.session.delete(btc_price)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
