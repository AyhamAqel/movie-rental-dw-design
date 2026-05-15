import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


def draw_table(ax, x, y, w, h, title, fields, color, edge):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.6,
        edgecolor=edge,
        facecolor=color
    )
    ax.add_patch(box)

    ax.add_patch(Rectangle((x, y), w * 0.36, h, linewidth=1.2,
                           edgecolor=edge, facecolor=color))

    ax.text(x + w * 0.18, y + h / 2, title,
            ha="center", va="center", fontsize=10, fontweight="bold")

    ax.text(x + w * 0.40, y + h - 0.18, "\n".join(fields),
            ha="left", va="top", fontsize=8)


def connect(ax, x1, y1, x2, y2):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", linewidth=1.4, color="#1f3b5c")
    )


def main():
    os.makedirs("visuals", exist_ok=True)

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    dim_color = "#d9ecff"
    fact_color = "#fff2b8"
    edge_color = "#1f4e79"

    ax.text(
        8, 9.55,
        "Movie Rental Data Warehouse - Dimensional Model",
        ha="center",
        fontsize=18,
        fontweight="bold",
        color="#0d274d"
    )

    # Dimension tables - left side
    draw_table(ax, 0.4, 7.4, 4.1, 1.15, "Dim_Staff", [
        "• PK staff_key",
        "• staff_id",
        "• full_name",
        "• email",
        "• active",
        "• store_id"
    ], dim_color, edge_color)

    draw_table(ax, 0.4, 5.9, 4.1, 1.3, "Dim_Customer", [
        "• PK customer_key",
        "• customer_id",
        "• full_name",
        "• email",
        "• active",
        "• city",
        "• country"
    ], dim_color, edge_color)

    draw_table(ax, 0.4, 4.35, 4.1, 1.25, "Dim_Store", [
        "• PK store_key",
        "• store_id",
        "• manager_staff_id",
        "• city",
        "• country"
    ], dim_color, edge_color)

    draw_table(ax, 0.4, 2.8, 4.1, 1.3, "Dim_Date", [
        "• PK date_key",
        "• full_date",
        "• day",
        "• month",
        "• quarter",
        "• year",
        "• day_name"
    ], dim_color, edge_color)

    draw_table(ax, 0.4, 1.05, 4.1, 1.45, "Dim_Film", [
        "• PK film_key",
        "• film_id",
        "• film_title",
        "• language_name",
        "• category_name",
        "• rental_duration",
        "• rental_rate",
        "• rating"
    ], dim_color, edge_color)

    # Fact tables - center/right
    draw_table(ax, 6.1, 6.75, 4.7, 1.7, "Fact_Payment", [
        "• PK payment_fact_key",
        "• DD payment_id",
        "• DD rental_id",
        "• FK payment_date_key",
        "• FK customer_key",
        "• FK film_key",
        "• FK store_key",
        "• FK staff_key",
        "",
        "Measures:",
        "  - payment_amount",
        "  - payment_count"
    ], fact_color, "#b58b00")

    draw_table(ax, 6.1, 4.1, 4.7, 2.05, "Fact_Rental", [
        "• PK rental_fact_key",
        "• DD rental_id",
        "• FK rental_date_key",
        "• FK return_date_key",
        "• FK customer_key",
        "• FK film_key",
        "• FK store_key",
        "• FK staff_key",
        "",
        "Measures:",
        "  - rental_count",
        "  - rental_duration_days",
        "  - late_return_flag"
    ], fact_color, "#b58b00")

    draw_table(ax, 6.1, 1.45, 4.7, 1.75, "Fact_Inventory", [
        "• PK inventory_fact_key",
        "• DD inventory_id",
        "• FK film_key",
        "• FK store_key",
        "",
        "Measures:",
        "  - inventory_count",
        "  - available_flag"
    ], fact_color, "#b58b00")

    # Connections to Fact_Payment
    connect(ax, 4.5, 7.95, 6.1, 7.65)   # staff
    connect(ax, 4.5, 6.55, 6.1, 7.45)   # customer
    connect(ax, 4.5, 4.95, 6.1, 7.25)   # store
    connect(ax, 4.5, 3.45, 6.1, 7.05)   # date
    connect(ax, 4.5, 1.75, 6.1, 6.90)   # film

    # Connections to Fact_Rental
    connect(ax, 4.5, 7.9, 6.1, 5.35)    # staff
    connect(ax, 4.5, 6.5, 6.1, 5.15)    # customer
    connect(ax, 4.5, 4.95, 6.1, 4.95)   # store
    connect(ax, 4.5, 3.45, 6.1, 4.75)   # date
    connect(ax, 4.5, 1.75, 6.1, 4.55)   # film

    # Connections to Fact_Inventory
    connect(ax, 4.5, 4.85, 6.1, 2.35)   # store
    connect(ax, 4.5, 1.75, 6.1, 2.15)   # film

    # Legend
    legend_x, legend_y = 0.5, 0.15
    ax.add_patch(Rectangle((legend_x, legend_y), 0.35, 0.22,
                           facecolor=dim_color, edgecolor=edge_color))
    ax.text(0.95, legend_y + 0.11, "Dimension Table", va="center", fontsize=9)

    ax.add_patch(Rectangle((legend_x + 2.1, legend_y), 0.35, 0.22,
                           facecolor=fact_color, edgecolor="#b58b00"))
    ax.text(2.95, legend_y + 0.11, "Fact Table", va="center", fontsize=9)

    output_path = "visuals/warehouse_star_schema.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Diagram saved successfully: {output_path}")


if __name__ == "__main__":
    main()