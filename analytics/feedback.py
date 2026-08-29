from config import get_connection


def save_feedback(
    persona,
    insight_text,
    rating,
    correction,
    confidence_score,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO insight_feedback
        (
            persona,
            insight_text,
            rating,
            correction,
            confidence_score
        )
        VALUES
        (%s, %s, %s, %s, %s)
        """,
        (
            persona,
            insight_text,
            rating,
            correction,
            confidence_score,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()