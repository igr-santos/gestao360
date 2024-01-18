from django.db import connection


def view_split_songs(stakeholder, report, order_by=["title"]):
    rows = []
    query = f"""
    SELECT
        UPPER(title) as title,
        round(SUM(amount)::numeric, 2) as amount,
        round(SUM(exchange_amount)::numeric, 2) as exchange_amount,
        split,
        round(SUM(income)::numeric, 2) as income,
        round(SUM(exchange_income)::numeric, 2) as exchange_income
    FROM public.view_split_songs
    WHERE distributionreport_id = {report.id}
    AND stakeholder_id = {stakeholder.id}
    GROUP BY title, split
    ORDER BY {",".join(order_by)}
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        # rows = cursor.fetchall()
        for row in cursor.fetchall():
            title, amount, exchange_amount, split, income, exchange_income = row
            rows.append(
                dict(
                    title=title,
                    amount=amount,
                    exchange_amount=exchange_amount,
                    split=split,
                    income=income,
                    exchange_income=exchange_income,
                )
            )

    return rows


def view_reports(stakeholder, start_date):
    rows = []
    query = f"""
    select
        rd.title,
        sum(vss.amount) as amount,
        sum(vss.exchange_amount) as exchange_amount,
        sum(vss.income) as income,
        sum(vss.exchange_income) as exchange_income
    from view_split_songs vss
    inner join reports_distributionreport rd on rd.id = vss.distributionreport_id
    where rd.start_date >= '{start_date}' and vss.stakeholder_id = {stakeholder.id} and rd.income is not null
    group by rd.title, rd.start_date
    order by rd.start_date
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        # rows = cursor.fetchall()
        for row in cursor.fetchall():
            title, amount, exchange_amount, income, exchange_income = row
            rows.append(
                dict(
                    title=title,
                    amount=amount,
                    exchange_amount=exchange_amount,
                    income=income,
                    exchange_income=exchange_income,
                )
            )
    
    return rows