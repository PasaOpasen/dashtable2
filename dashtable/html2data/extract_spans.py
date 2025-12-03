
from typing import Optional

from ..dashutils.aliases import DATA_SPANS
from ..dashutils import get_span, convert_spans_to_array, get_span_index


def extract_spans(html_string: str) -> Optional[DATA_SPANS]:
    """
    Creates a list of the spanned cell groups of [row, column] pairs.

    Parameters
    ----------
    html_string : str

    Returns
    -------
    list of lists of lists of int
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: You must have BeautifulSoup to use html2data")
        return

    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if not table:
        return []

    trs = table.find_all('tr')
    if len(trs) == 0:
        return []

    spans = []
    spans_arr = None

    for tr in range(len(trs)):
        if tr == 0:
            ths = trs[tr].find_all('th')
            if len(ths) == 0:
                ths = trs[tr].find_all('td')
            tds = ths
        else:
            tds = trs[tr].find_all('td')

        if spans_arr is None:
            column = 0
        else:
            filled_columns = spans_arr[spans_arr[:, 1] == tr, 2]
            """already used columns for current row"""

            column = next(
                c for c in range(filled_columns.max() + 2) if c not in filled_columns
            ) if filled_columns.size else 0

        for td in tds:
            r_span_count = 1
            c_span_count = 1
            current_column = column

            if td.has_attr('rowspan'):
                r_span_count = int(td['rowspan'])
            if td.has_attr('colspan'):
                c_span_count = int(td['colspan'])
                column += c_span_count
            else:
                column += 1

            new_span = []
            for r_index in range(tr, tr + r_span_count):
                for c_index in range(current_column, column):
                    if not (
                        spans and
                        get_span_index(spans_arr, r_index, c_index) is not None
                    ):
                        new_span.append((r_index, c_index))

            if new_span:
                spans.append(new_span)
                spans_arr = convert_spans_to_array(spans)

    return spans
