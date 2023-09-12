import loguru
import pyspark.sql
import ujson
from pyspark.ml import feature
from pyspark.sql import types, functions

FEATURES_COLUMN = "scaled_feature"


def preprocess(
    df: pyspark.sql.DataFrame,
    columns_filename: str,
) -> pyspark.sql.DataFrame:
    with open(columns_filename, "r") as columns_file:
        columns = ujson.load(columns_file)

    id_columns = columns["id"]
    feature_column_names = columns["nutriments"]
    feature_columns = [
        functions.col(c).cast("float").alias(c) for c in feature_column_names
    ]
    cat_columns = columns["categories"]

    all_columns = id_columns + feature_columns + cat_columns
    df_with_selected_columns = df.select(*all_columns)

    vec_assembler = feature.VectorAssembler(
        inputCols=feature_column_names, outputCol="features"
    )
    df_with_features = vec_assembler.transform(df_with_selected_columns)

    scaler = feature.StandardScaler(inputCol="features", outputCol=FEATURES_COLUMN)
    scaler_model = scaler.fit(df_with_features)
    df_scaled_features = scaler_model.transform(df_with_features)
    return df_scaled_features
