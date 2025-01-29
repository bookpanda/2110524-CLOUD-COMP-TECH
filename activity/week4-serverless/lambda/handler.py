import json


def lambda_handler(event, context):
    # TODO implement
    try:
        body = json.loads(event["body"])
        a = int(body.get("a", "9"))
        b = int(body.get("b", "6"))
        op = body.get("op", "+")

        result = a
        match op:
            case "+":
                result += b
            case "-":
                result -= b
            case "*":
                result *= b
            case "/":
                result /= b

        return {"statusCode": 200, "body": json.dumps({"result": result})}

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in body"}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
