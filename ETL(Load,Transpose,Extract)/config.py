"""
==========================================================
Configuration Module
Customer Revenue Opportunity Intelligence Platform

Purpose:
    Stores dataset-specific configuration for the ETL pipeline.

Author:
    Your Name
==========================================================
"""

from pathlib import Path

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------
RAW_DATA_PATH = Path("Dataset") / "raw"
PROCESSED_DATA_PATH = Path("Dataset") / "processed"
REPORT_PATH = Path("reports")

# ---------------------------------------------------------
# Dataset Configurations
# ---------------------------------------------------------

DATASETS = {

 # =====================================================
# Customers Dataset
# =====================================================

"customers": {

    "input_file": "olist_customers_dataset.csv",

    "output_file": "olist_customers_dataset_cleaned.csv",

    "primary_key": "customer_id",

    "required_columns": [

        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"

    ],

    "numeric_columns": [

        "customer_zip_code_prefix"

    ],

    "date_columns": [

    ],

    "title_columns": [

        "customer_city"

    ],

    "upper_columns": [

        "customer_state"

    ],

    "lower_columns": [

    ],

    # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must never be NULL
        "not_null_columns": [

            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"

        ],

        # customer_id must be unique
        "unique_columns": [

            "customer_id"

        ],

        # Numeric validation
        "numeric_ranges": {

            "customer_zip_code_prefix": (1, None)

        }

    }

},


# =====================================================
# Orders Dataset
# =====================================================

"orders": {

    "input_file": "olist_orders_dataset.csv",

    "output_file": "olist_orders_dataset_cleaned.csv",

    "primary_key": "order_id",

    "required_columns": [

        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp"

    ],

    "numeric_columns": [

    ],

    "date_columns": [

        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"

    ],

    "title_columns": [

    ],

    "upper_columns": [

    ],

    "lower_columns": [

        "order_status"

    ],

    "validation": {

        "not_null_columns": [

            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp"

        ],

        "unique_columns": [

            "order_id"

        ],

        "allowed_values": {

            "order_status": [

                "approved",
                "processing",
                "shipped",
                "delivered",
                "invoiced",
                "created",
                "unavailable",
                "canceled"

            ]

        },

        "date_sequences": [

            (
                "order_purchase_timestamp",
                "order_approved_at"
            ),

            (
                "order_purchase_timestamp",
                "order_delivered_customer_date"
            ),

            (
                "order_purchase_timestamp",
                "order_estimated_delivery_date"
            ),
            (
                "order_approved_at",
                "order_delivered_customer_date"
               )

        ],

        "foreign_keys": [

            {

                "column": "customer_id",

                "reference_dataset": "customers",

                "reference_column": "customer_id"

            }

        ]

    }

},


# =====================================================
# Order Items Dataset
# =====================================================

"order_items": {

    "input_file": "olist_order_items_dataset.csv",

    "output_file": "olist_order_items_dataset_cleaned.csv",

    "primary_key": "order_id",

    "required_columns": [

        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"

    ],

    "numeric_columns": [

        "order_item_id",
        "price",
        "freight_value"

    ],

    "date_columns": [

        "shipping_limit_date"

    ],

    "title_columns": [

    ],

    "upper_columns": [

    ],

    "lower_columns": [

    ],

    "validation": {

        "not_null_columns": [

            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "price",
            "freight_value"

        ],

        "composite_unique_columns": [

            [

                "order_id",

                "order_item_id"

            ]

        ],

        "numeric_ranges": {

            "price": (0, None),

            "freight_value": (0, None)

        },

        "foreign_keys": [

            {

                "column": "order_id",

                "reference_dataset": "orders",

                "reference_column": "order_id"

            },

            {

                "column": "product_id",

                "reference_dataset": "products",

                "reference_column": "product_id"

            },

            {

                "column": "seller_id",

                "reference_dataset": "sellers",

                "reference_column": "seller_id"

            }

        ]

    }

},

    # =====================================================
    # Products Dataset
    # =====================================================

    "products": {

        "input_file": "olist_products_dataset.csv",

        "output_file": "olist_products_dataset_cleaned.csv",

        "primary_key": "product_id",

        "required_columns": [

            "product_id"

        ],

        "numeric_columns": [

            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"

        ],

        "date_columns": [

        ],

        "title_columns": [

        ],

        "upper_columns": [

        ],

        "lower_columns": [

            "product_category_name"

        ],
            # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must not contain NULL values
        "not_null_columns": [

            "product_id"

        ],

        # Product ID must be unique
        "unique_columns": [

            "product_id"

        ],

        # Numeric validations
        "numeric_ranges": {

            "product_name_lenght": (0, None),

            "product_description_lenght": (0, None),

            "product_photos_qty": (0, None),

            "product_weight_g": (0, None),

            "product_length_cm": (0, None),

            "product_height_cm": (0, None),

            "product_width_cm": (0, None)

        }

    }

},


    # =====================================================
    # Sellers Dataset
    # =====================================================

    "sellers": {

        "input_file": "olist_sellers_dataset.csv",

        "output_file": "olist_sellers_dataset_cleaned.csv",

        "primary_key": "seller_id",

        "required_columns": [

            "seller_id",
            "seller_city",
            "seller_state"

        ],

        "numeric_columns": [

            "seller_zip_code_prefix"

        ],

        "date_columns": [

        ],

        "title_columns": [

            "seller_city"

        ],

        "upper_columns": [

            "seller_state"

        ],

        "lower_columns": [

        ],
            # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must not contain NULL values
        "not_null_columns": [

            "seller_id",
            "seller_city",
            "seller_state"

        ],

        # Seller ID must be unique
        "unique_columns": [

            "seller_id"

        ],

        # Numeric validation
        "numeric_ranges": {

            "seller_zip_code_prefix": (1, None)

        }

    }

    },

    # =====================================================
# Payments Dataset
# =====================================================

"payments": {

    "input_file": "olist_order_payments_dataset.csv",

    "output_file": "olist_order_payments_dataset_cleaned.csv",

    "primary_key": "order_id",

    "required_columns": [

        "order_id",
        "payment_type",
        "payment_value"

    ],

    "numeric_columns": [

        "payment_sequential",
        "payment_installments",
        "payment_value"

    ],

    "date_columns": [

    ],

    "title_columns": [

    ],

    "upper_columns": [

    ],

    "lower_columns": [

        "payment_type"

    ],

    # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must never be NULL
        "not_null_columns": [

            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"

        ],

        # Composite Primary Key
        "composite_unique_columns": [

            [
                "order_id",
                "payment_sequential"
            ]

        ],

        # Numeric Validation
        "numeric_ranges": {

            "payment_sequential": (1, None),

            "payment_installments": (0, None),

            "payment_value": (0, None)

        },

        # Allowed Payment Types
        "allowed_values": {

            "payment_type": [

                "credit_card",
                "boleto",
                "voucher",
                "debit_card",
                "not_defined"

            ]

        },

        # Foreign Key Validation
        "foreign_keys": [

            {

                "column": "order_id",

                "reference_dataset": "orders",

                "reference_column": "order_id"

            }

        ]

    }

},

    
    # =====================================================
    # Reviews Dataset
    # =====================================================

    "reviews": {

        "input_file": "olist_order_reviews_dataset.csv",

        "output_file": "olist_order_reviews_dataset_cleaned.csv",

        "primary_key": "review_id",

        "required_columns": [

            "review_id",
            "order_id",
            "review_score"

        ],

        "numeric_columns": [

            "review_score"

        ],

        "date_columns": [

            "review_creation_date",
            "review_answer_timestamp"

        ],

        "title_columns": [

        ],

        "upper_columns": [

        ],

        "lower_columns": [

        ],
            # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must not contain NULL values
        "not_null_columns": [

            "review_id",
            "order_id",
            "review_score"

        ],

        # Review ID must be unique
        "composite_unique_columns": [
    ["review_id", "order_id"]
],

        # Review score should be between 1 and 5
        "numeric_ranges": {

            "review_score": (1, 5)

        },

       
        # Date sequence validation
        "date_sequences": [

            (

                "review_creation_date",

                "review_answer_timestamp"

            )

        ],

        # Foreign Key Validation
        "foreign_keys": [

            {

                "column": "order_id",

                "reference_dataset": "orders",

                "reference_column": "order_id"

            }

        ]
    }

    },

    # =====================================================
    # Geolocation Dataset
    # =====================================================

    "geolocation": {

        "input_file": "olist_geolocation_dataset.csv",

        "output_file": "olist_geolocation_dataset_cleaned.csv",

        "primary_key": "geolocation_zip_code_prefix",

        "required_columns": [

            "geolocation_zip_code_prefix",
            "geolocation_city",
            "geolocation_state"

        ],

        "numeric_columns": [

            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"

        ],

        "date_columns": [

        ],

        "title_columns": [

            "geolocation_city"

        ],

        "upper_columns": [

            "geolocation_state"

        ],

        "lower_columns": [

        ],
            # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must not contain NULL values
        "not_null_columns": [

            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state"

        ],

        # Latitude and Longitude validation
        "numeric_ranges": {

            "geolocation_lat": (-90, 90),

            "geolocation_lng": (-180, 180),

            "geolocation_zip_code_prefix": (1, None)

        }

    }

    },

    # =====================================================
# Category Translation Dataset
# =====================================================

"category_translation": {

    "input_file": "product_category_name_translation.csv",

    "output_file": "product_category_name_translation_cleaned.csv",

    "primary_key": "product_category_name",

    "required_columns": [

        "product_category_name",
        "product_category_name_english"

    ],

    "numeric_columns": [

    ],

    "date_columns": [

    ],

    "title_columns": [

        "product_category_name_english"

    ],

    "upper_columns": [

    ],

    "lower_columns": [

        "product_category_name"

    ],

    # -------------------------------------------------
    # Validation Rules
    # -------------------------------------------------

    "validation": {

        # Columns that must not contain NULL values
        "not_null_columns": [

            "product_category_name",
            "product_category_name_english"

        ],

        # Product category name must be unique
        "unique_columns": [

            "product_category_name"

        ]

    }

}
}


if __name__ == "__main__":
    print(DATASETS.keys())