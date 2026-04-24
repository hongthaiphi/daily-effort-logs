"""Dashboard - Generate charts"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
from typing import List, Tuple

CHARTS_DIR = "charts"

# Create charts directory if not exists
os.makedirs(CHARTS_DIR, exist_ok=True)

def create_chart(user_id: int, scores: List[Tuple[str, int, str]]) -> str:
    """
    Create a line chart for effort scores

    Args:
        user_id: User ID
        scores: List of (date, score, diary) tuples, sorted DESC by date

    Returns:
        Path to the generated chart image
    """
    if not scores:
        return None

    # Reverse to get ascending order by date
    scores = list(reversed(scores))

    dates = [datetime.strptime(date, '%Y-%m-%d') for date, _, _ in scores]
    values = [score for _, score, _ in scores]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot line
    ax.plot(dates, values, marker='o', linewidth=2, markersize=8, color='#2196F3')
    ax.fill_between(dates, values, alpha=0.3, color='#2196F3')

    # Format chart
    ax.set_xlabel('Ngày', fontsize=12, fontweight='bold')
    ax.set_ylabel('Điểm nỗ lực (1-10)', fontsize=12, fontweight='bold')
    ax.set_title('📊 Biểu đồ nỗ lực - 30 ngày', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 11)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    fig.autofmt_xdate(rotation=45, ha='right')

    # Add average line
    avg = sum(values) / len(values)
    ax.axhline(y=avg, color='#FF9800', linestyle='--', linewidth=2, label=f'Trung bình: {avg:.1f}')
    ax.legend(fontsize=10)

    # Save chart
    chart_path = os.path.join(CHARTS_DIR, f"effort_chart_{user_id}.png")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=100, bbox_inches='tight')
    plt.close()

    return chart_path

def create_stats_image(user_id: int, stats: dict) -> str:
    """
    Create a simple stats visualization

    Args:
        user_id: User ID
        stats: Dictionary with avg_score, max_score, min_score, total_days

    Returns:
        Path to the generated image
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')

    # Title
    fig.text(0.5, 0.95, '📊 Thống kê nỗ lực', ha='center', fontsize=18, fontweight='bold')

    # Stats text
    stats_text = (
        f"📈 Điểm trung bình: {stats['avg_score']}/10\n\n"
        f"🔝 Điểm cao nhất: {stats['max_score']}/10\n\n"
        f"🔻 Điểm thấp nhất: {stats['min_score']}/10\n\n"
        f"📅 Tổng ngày ghi: {stats['total_days']} ngày"
    )

    fig.text(0.5, 0.5, stats_text, ha='center', va='center', fontsize=14,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Save image
    chart_path = os.path.join(CHARTS_DIR, f"stats_{user_id}.png")
    plt.savefig(chart_path, dpi=100, bbox_inches='tight')
    plt.close()

    return chart_path
