from django import template

register = template.Library()


@register.filter
def convert_data_frame_to_html_table_headers(df):
    html = "<tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"

    html += "</tr>"
    return html


@register.filter
def convert_data_frame_to_html_table_rows(df):
    html = ""
    for row in df.values:
        row_html = "<tr>"
        for value in row:
            row_html += f"<td>{value}</td>"
        row_html += "</tr>"
        html += row_html

    return html
