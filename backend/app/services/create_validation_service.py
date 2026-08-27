from app.models.models import Validations


def create_validation_record(
    db,
    invoice_id,
    validation_type,
    result
):

    validation = Validations(
        invoice_id=invoice_id,
        validation_type=validation_type,
        status=result["status"],
        message=result["message"] if "message" in result else result["reason"],
        expected_value=result.get("expected_value"),
        actual_value=result.get("actual_value"),
        difference=result.get("difference")
    )

    db.add(validation)

    return validation