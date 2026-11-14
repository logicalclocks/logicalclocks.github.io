---
description: The ecommerce semantic layer blueprint of the Hopsworks Factory, which builds an online shop's orders as feature groups, a semantic project of sales metrics and a chat app in which an LLM turns questions into metric queries.
---

# Ecommerce Blueprint { #semantic-ecommerce-blueprint }

The Factory's **Analytics > Blueprints > Ecommerce orders semantic layer** builds a complete semantic layer for an online shop's sales, from generated data to a chat app.
It is the canonical example of a semantic layer on Hopsworks: metrics defined once over feature groups and sliced by any time range, region, customer group, product or channel.

The build creates:

- four feature groups of generated orders, written by a backfill of two years and a daily job;
- the semantic project `<name>`, the blueprint's dbt project with four semantic models, 26 metrics and three saved queries;
- the app `<name>-chat`, where questions in plain language are translated by an LLM into metric queries.

## Build it { #semantic-ecommerce-blueprint-build }

=== "UI"

    In the project's **Factory**, open **New > Analytics > Blueprints** and pick **Ecommerce orders semantic layer**.
    The form asks for the name (`ecommerce-semantic` by default), the repository, and the LLM of the chat app.
    **Create** starts the build in the Terminal, where Claude Code runs `/hops-semantic-layer <name>`, and the Factory shows its phases.

=== "CLI"

    ```bash
    hops factory run analytics-semantic --preset ecommerce-orders-example
    ```

The build runs six phases, recorded in the system's `system.yaml`:

| Phase | Does |
| --- | --- |
| Test the generator and app | Runs the tests of the generator and of the app's translator. |
| Backfill history | Writes two years of history up to the last midnight (UTC) with the job `<name>-backfill`. |
| Register and compile metrics | Writes the time spine, registers the dbt project as the semantic project and compiles it; `hops semantic test` runs every metric once. |
| Reconcile metrics | Checks that the totals of nine metrics equal SQL over the feature groups, and runs the saved queries. |
| Deploy the chat app | Deploys `<name>-chat` and smoke-tests it. |
| Schedule the daily job | Schedules `<name>-daily`, which writes each new day. |

## The data { #semantic-ecommerce-blueprint-data }

The generator writes a star schema around order lines, each table an offline Delta feature group tagged `analytics_table` `{"layer": "gold"}`.

| Feature group | One row per | Columns |
| --- | --- | --- |
| `ecommerce_order_items` | order line | `order_id`, `customer_id`, `product_id`, `ordered_at`, `status`, `quantity`, `unit_price`, `gross_amount`, `discount_amount`, `net_amount`, `cost_amount`, `profit_amount` |
| `ecommerce_orders` | order | `customer_id`, `ordered_at`, `channel`, `payment_method`, `promotion`, `status`, `customer_type`, `item_count`, `units`, the order's amounts and `shipping_fee` |
| `ecommerce_customers` | customer | `region`, `country`, `city`, `segment`, `loyalty_tier`, `acquisition_channel`, `signup_ts`, `signup_month` |
| `ecommerce_products` | product | `product_name`, `category`, `subcategory`, `brand`, `price_band`, `list_price`, `unit_cost`, `launched_at` |

The two years hold about 160,000 orders.
Volume grows about 30% a year, faster in Asia Pacific and Latin America; weekends are busier, January is quiet, November and December peak around Black Friday and Cyber Monday, and site-wide sales discount most orders on their days.
Every row is a function of its day, so a replayed day rewrites the same rows.

## The metrics { #semantic-ecommerce-blueprint-metrics }

All money is in USD, without shipping, and relates as `gross_sales - discounts - returns = revenue` and `revenue - cost_of_goods_sold = gross_profit`.
Cancelled orders count in no money metric; a returned order is refunded in full.

| Metric | Type | Meaning |
| --- | --- | --- |
| `revenue` | simple | Net revenue: what customers paid for the items they kept. |
| `gross_sales`, `discounts`, `returns` | simple | List value before discounts, discounts given, and refunds. |
| `cost_of_goods_sold`, `gross_profit` | simple | Cost of the units kept, and revenue minus that cost. |
| `gross_margin` | ratio | Gross profit over net revenue. |
| `orders`, `completed_orders`, `returned_orders`, `cancelled_orders`, `all_orders` | simple | Orders by status; `orders` excludes cancelled ones. |
| `average_order_value`, `units_per_order` | ratio | Net revenue and units per completed order. |
| `units_sold`, `buyers`, `revenue_per_buyer` | simple, ratio | Units kept, distinct customers who ordered, and revenue per buyer. |
| `discount_rate`, `return_rate`, `cancellation_rate` | ratio | Shares from 0 to 1. |
| `shipping_revenue`, `new_customers` | simple | Shipping charged on completed orders, and signups by signup date. |
| `revenue_month_to_date`, `revenue_trailing_28d` | cumulative | Month to date and trailing 28 days; grouped by `metric_time`. |
| `revenue_last_year`, `revenue_growth_yoy` | derived, offset | The same period a year earlier, and the growth against it; grouped by `metric_time`. |

The dimensions are `metric_time` at any grain, the customer's `customer__region`, `customer__country`, `customer__city`, `customer__segment`, `customer__loyalty_tier`, `customer__acquisition_channel` and `customer__signup_month`, the order's `order__channel`, `order__payment_method`, `order__promotion`, `order__status` and `order__customer_type`, and the product's `product__category`, `product__subcategory`, `product__brand` and `product__price_band`.
The order metrics cannot be grouped by product, since an order has several.

```bash
hops semantic query ecommerce_semantic --metrics revenue,average_order_value \
  --group-by metric_time__quarter,customer__segment --start-time 2026-01-01
hops semantic query ecommerce_semantic --metrics revenue_growth_yoy --group-by metric_time__month
hops semantic query ecommerce_semantic --saved-query category_performance_quarterly
```

## The chat app { #semantic-ecommerce-blueprint-chat }

`<name>-chat` answers questions such as "net revenue by region per quarter this year" or "which customer segment had the highest average order value last quarter?".
Each answer shows one sentence on what the query shows, the query itself, a chart, the rows and the SQL; a follow-up such as "only Europe" refines the previous query.
**Edit query** changes an answer's metrics, group-bys, filters and time range and runs it again, and **Build a query** writes one from scratch, both without the LLM.

The LLM is any OpenAI-compatible chat endpoint, set as the account environment variables of the member who starts the app:

| Variable | Value |
| --- | --- |
| `LLM_URL` | The endpoint's base URL, such as `https://api.openai.com/v1`, or the OpenAI URL of an LLM deployment in the project. |
| `LLM_MODEL` | The model name. |
| `LLM_API_KEY` | The key the endpoint takes. |

The blueprint's form saves them; without them the app answers no questions but its query builder works.
Change them in **Account settings > Environment variables** and restart the app.

The LLM writes the query, never the answer:

- it sees the semantic project's metrics and dimensions, with the values of the small dimensions, and the question, never a data row;
- it answers with a JSON query of metrics, group-bys, filters, a time range, an order and a limit;
- the app refuses a name the catalog lacks, a filter value a dimension does not take and a group-by a metric cannot reach, and sends the reason back to the LLM once;
- the query runs through the semantic layer as the member who started the app, with the filter values bound as literals, never as SQL.
