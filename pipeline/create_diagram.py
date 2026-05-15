import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch


def draw_table(ax, x, y, w, h, title, fields,
               header_color, body_color, edge_color):

    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.5,
        edgecolor=edge_color,
        facecolor=body_color
    )

    ax.add_patch(box)

    header_h = 0.42

    ax.add_patch(Rectangle(
        (x, y + h - header_h),
        w,
        header_h,
        facecolor=header_color,
        edgecolor=edge_color,
        linewidth=1.2
    ))

    ax.text(
        x + w / 2,
        y + h - header_h / 2,
        title,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="white"
    )

    ax.text(
        x + 0.2,
        y + h - header_h - 0.18,
        "\n".join(fields),
        ha="left",
        va="top",
        fontsize=8.3,
        linespacing=1.3
    )


def connect(ax, start, end):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.3,
            color="#2c3e50"
        )
    )


def main():

    os.makedirs("visuals", exist_ok=True)

    fig, ax = plt.subplots(figsize=(18, 11))

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)

    ax.axis("off")

    # Colors
    dim_header = "#1565c0"
    dim_body = "#e8f1ff"

    fact_header = "#2e7d32"
    fact_body = "#edf7ee"

    edge_color = "#1f2937"

    # Title
    ax.text(
        9,
        13.4,
        "Movie Rental Data Warehouse - Dimensional Model",
        ha="center",
        fontsize=22,
        fontweight="bold",
        color="#0f172a"
    )

    ax.plot(
        [0.5, 17.5],
        [13.05, 13.05],
        color="#0f172a",
        linewidth=1.5
    )

    # =========================
    # DIMENSIONS
    # =========================

    draw_table(ax, 0.8, 10.7, 4.2, 1.8,
               "Dim_Staff",
               [
                   "• PK  staff_key",
                   "• staff_id",
                   "• full_name",
                   "• email",
                   "• active",
                   "• store_id"
               ],
               dim_header,
               dim_body,
               edge_color)

    draw_table(ax, 0.8, 8.35, 4.2, 2.0,
               "Dim_Customer",
               [
                   "• PK  customer_key",
                   "• customer_id",
                   "• full_name",
                   "• email",
                   "• active",
                   "• address",
                   "• city",
                   "• country"
               ],
               dim_header,
               dim_body,
               edge_color)

    draw_table(ax, 0.8, 5.95, 4.2, 1.8,
               "Dim_Store",
               [
                   "• PK  store_key",
                   "• store_id",
                   "• manager_staff_id",
                   "• address",
                   "• city",
                   "• country"
               ],
               dim_header,
               dim_body,
               edge_color)

    draw_table(ax, 0.8, 3.15, 4.2, 2.2,
               "Dim_Date",
               [
                   "• PK  date_key",
                   "• full_date",
                   "• day",
                   "• month",
                   "• quarter",
                   "• year",
                   "• day_name"
               ],
               dim_header,
               dim_body,
               edge_color)

    draw_table(ax, 0.8, 0.55, 4.2, 2.3,
               "Dim_Film",
               [
                   "• PK  film_key",
                   "• film_id",
                   "• film_title",
                   "• release_year",
                   "• language_name",
                   "• category_name",
                   "• rental_duration",
                   "• rental_rate",
                   "• rating"
               ],
               dim_header,
               dim_body,
               edge_color)

    # =========================
    # FACT TABLES
    # =========================

    draw_table(ax, 8.2, 9.65, 5.2, 2.7,
               "Fact_Payment",
               [
                   "• PK  payment_fact_key",
                   "• DD  payment_id",
                   "• DD  rental_id",
                   "• FK  payment_date_key",
                   "• FK  customer_key",
                   "• FK  film_key",
                   "• FK  store_key",
                   "• FK  staff_key",
                   "",
                   "Measures:",
                   "  - payment_amount",
                   "  - payment_count"
               ],
               fact_header,
               fact_body,
               edge_color)

    draw_table(ax, 8.2, 5.75, 5.2, 3.2,
               "Fact_Rental",
               [
                   "• PK  rental_fact_key",
                   "• DD  rental_id",
                   "• FK  rental_date_key",
                   "• FK  return_date_key",
                   "• FK  customer_key",
                   "• FK  film_key",
                   "• FK  store_key",
                   "• FK  staff_key",
                   "",
                   "Measures:",
                   "  - rental_count",
                   "  - rental_duration_days",
                   "  - late_return_flag"
               ],
               fact_header,
               fact_body,
               edge_color)

    draw_table(ax, 8.2, 1.35, 5.2, 2.6,
               "Fact_Inventory",
               [
                   "• PK  inventory_fact_key",
                   "• DD  inventory_id",
                   "• FK  film_key",
                   "• FK  store_key",
                   "",
                   "Measures:",
                   "  - inventory_count",
                   "  - available_flag"
               ],
               fact_header,
               fact_body,
               edge_color)

    # =========================
    # CONNECTIONS
    # =========================

    # Payment
    connect(ax, (5.0, 11.6), (8.2, 11.5))
    connect(ax, (5.0, 9.4), (8.2, 11.1))
    connect(ax, (5.0, 6.9), (8.2, 10.7))
    connect(ax, (5.0, 4.3), (8.2, 10.3))
    connect(ax, (5.0, 1.9), (8.2, 9.9))

    # Rental
    connect(ax, (5.0, 11.4), (8.2, 7.9))
    connect(ax, (5.0, 9.2), (8.2, 7.5))
    connect(ax, (5.0, 6.8), (8.2, 7.1))
    connect(ax, (5.0, 4.1), (8.2, 6.7))
    connect(ax, (5.0, 1.8), (8.2, 6.3))

    # Inventory
    connect(ax, (5.0, 6.7), (8.2, 2.8))
    connect(ax, (5.0, 1.7), (8.2, 2.4))

    # Legend
    ax.add_patch(Rectangle(
        (0.8, 0.1),
        0.45,
        0.28,
        facecolor=dim_body,
        edgecolor=edge_color
    ))

    ax.text(
        1.45,
        0.24,
        "Dimension Table",
        fontsize=10,
        va="center"
    )

    ax.add_patch(Rectangle(
        (3.2, 0.1),
        0.45,
        0.28,
        facecolor=fact_body,
        edgecolor=edge_color
    ))

    ax.text(
        3.85,
        0.24,
        "Fact Table",
        fontsize=10,
        va="center"
    )

    output_path = "visuals/warehouse_star_schema.png"

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"Diagram saved successfully: {output_path}")


if __name__ == "__main__":
    main()