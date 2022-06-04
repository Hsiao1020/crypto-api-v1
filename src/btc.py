from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from flasgger import swag_from

from src.database import BTC, db
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

btc = Blueprint("btc", __name__, url_prefix="/api/v1/btc")


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

        return jsonify({
            "btc_datetime": btc_price.btc_datetime,
            "Open": btc_price.Open,
            "High": btc_price.High,
            "Low": btc_price.Low,
            "Close": btc_price.Close,
            "Adj_Close": btc_price.Adj_Close,
            "Volume": btc_price.Volume,
            "created_at": btc_price.created_at,
            "updated_at": btc_price.updated_at
        }), HTTP_201_CREATED

    else:
        # start = request.args.get("start", None)
        # end = request.args.get("end", datetime.now())

        # if start and end:
        #     try:
        #         datetime.strptime(start, "%Y-%m-%d")
        #         datetime.strptime(end, "%Y-%m-%d")
        #         qry = DBSession.query(User).filter(
        # and_(User.birthday <= '1988-01-17', User.birthday >= '1985-01-17'))
        #     except ValueError:
        #         return jsonify({"message": "Incorrect argument format, arguments start and end should be YYYY-MM-DD"})

        # elif start:
        #     try:
        #         datetime.strptime(start, "%Y-%m-%d")
        #     except ValueError:
        #         return jsonify({"message": "Incorrect argument format, arguments start and end should be YYYY-MM-DD"})

        # elif end:
        #     try:
        #         datetime.strptime(end, "%Y-%m-%d")
        #     except ValueError:
        #         return jsonify({"message": "Incorrect argument format, end argument should be YYYY-MM-DD"})

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        all_btc_price = BTC.query.filter_by().paginate(page=page, per_page=per_page)

        data = []

        for btc_price in all_btc_price.items:
            data.append({
                "btc_datetime": btc_price.btc_datetime,
                "Open": btc_price.Open,
                "High": btc_price.High,
                "Low": btc_price.Low,
                "Close": btc_price.Close,
                "Adj_Close": btc_price.Adj_Close,
                "Volume": btc_price.Volume,
                "created_at": btc_price.created_at,
                "updated_at": btc_price.updated_at
            })

            meta = {
                "page": all_btc_price.page,
                "pages": all_btc_price.pages,
                "total_count": all_btc_price.total,
                "prev_page": all_btc_price.prev_num,
                "next_page": all_btc_price.next_num,
                "has_next": all_btc_price.has_next,
                "has_prev": all_btc_price.has_prev,
            }

        return jsonify({"data": data, "meta": meta}), HTTP_200_OK
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

    return jsonify({
        "btc_datetime": btc_price.btc_datetime,
        "Open": btc_price.Open,
        "High": btc_price.High,
        "Low": btc_price.Low,
        "Close": btc_price.Close,
        "Adj_Close": btc_price.Adj_Close,
        "Volume": btc_price.Volume,
        "created_at": btc_price.created_at,
        "updated_at": btc_price.updated_at
    }), HTTP_200_OK


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

    return jsonify({
        "btc_datetime": btc_price.btc_datetime,
        "Open": btc_price.Open,
        "High": btc_price.High,
        "Low": btc_price.Low,
        "Close": btc_price.Close,
        "Adj_Close": btc_price.Adj_Close,
        "Volume": btc_price.Volume,
        "created_at": btc_price.created_at,
        "updated_at": btc_price.updated_at
    }), HTTP_200_OK


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
