import pandas as pd
from mock import Mock

import procompliance_test.models as models


def test_get_df_content(tmp_path):
    data = [
        ['A', 1.2, 2],
        ['B', 2.3, 3],
        ['C', 4.2, 4],
        ['A', 3.3, 2],
        ['A', 3.3, 3]
    ]
    df = pd.DataFrame(data, columns=['text_column', 'float_column', 'int_column'])
    path = tmp_path / '1.csv'
    df.to_csv(path, index=False)
    filter_query = 'text_column=="A"&float_column==3.3'
    models.get_dataset_path_by_id = Mock(return_value=path)
    returned_df = models.get_df_content(
        dataset_id=1,
        filter_query=filter_query
    )
    assert returned_df.equals(df.query(filter_query))
    returned_df = models.get_df_content(
        dataset_id=1,
        sort='text_column,int_column',
        order='asc,desc'
    )
    assert returned_df.equals(df.sort_values(['text_column', 'int_column'], ascending=[True, False]))
