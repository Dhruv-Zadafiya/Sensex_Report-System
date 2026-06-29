import os
import sys
import argparse
import logging

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.logging import RichHandler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

console = Console()

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(
            "logs/stock_updater.log",
            encoding="utf-8"
        ),
        RichHandler(
            rich_tracebacks=True,
            console=console
        )
    ]
)

logger = logging.getLogger("app")

from data.stock_fetcher import get_sensex_data
from reports.report_generator import generate_report
from email_service.mail_sender import send_mail
from data.db import (
    save_stock_data,
    get_recent_reports,
    is_db_connected
)
from scheduler.scheduler import start_scheduler


def run_job():
    """
    Fetch stock data -> Store in MongoDB -> Generate report -> Send Email
    """

    console.print(
        "\n[bold blue]Starting SENSEX Update Job...[/bold blue]"
    )

    try:
        # Fetch Data
        stock = get_sensex_data()

        open_price = stock["open"]
        close_price = stock["close"]
        date_str = stock["date"]

        console.print(
            f"[green]Fetched:[/green] {date_str}"
        )

        # Save to MongoDB
        db_id = save_stock_data(
            open_price,
            close_price,
            date_str
        )

        if db_id:
            console.print(
                f"[green]MongoDB Saved:[/green] {db_id}"
            )
        else:
            console.print(
                "[red]MongoDB Insert Failed[/red]"
            )

        # Generate Report
        report = generate_report(
            open_price,
            close_price,
            date_str
        )

        # Send Email
        email_status, message = send_mail(report)

        if email_status:
            console.print(
                "[green]Email Sent Successfully[/green]"
            )
        else:
            console.print(
                f"[red]Email Failed:[/red] {message}"
            )

        console.print(
            "[bold green]Job Completed Successfully[/bold green]"
        )

    except Exception as e:
        logger.exception("Job Failed")
        console.print(
            f"[bold red]Error:[/bold red] {e}"
        )


def show_dashboard():

    console.print(
        "\n[bold cyan]SENSEX MONITORING DASHBOARD[/bold cyan]\n"
    )

    db_status = (
        "Connected"
        if is_db_connected()
        else "Disconnected"
    )

    table = Table(
        title="System Status"
    )

    table.add_column("Service")
    table.add_column("Status")

    table.add_row(
        "MongoDB Atlas",
        db_status
    )

    console.print(table)

    reports = get_recent_reports(5)

    if reports:

        history = Table(
            title="Recent Reports"
        )

        history.add_column("Date")
        history.add_column("Open")
        history.add_column("Close")
        history.add_column("Change")

        for r in reports:

            history.add_row(
                str(r.get("trading_date")),
                str(r.get("open_price")),
                str(r.get("close_price")),
                str(r.get("change"))
            )

        console.print(history)

    else:

        console.print(
            "[yellow]No Reports Found[/yellow]"
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--run-once",
        action="store_true"
    )

    parser.add_argument(
        "--scheduler",
        action="store_true"
    )

    parser.add_argument(
        "--dashboard",
        action="store_true"
    )

    parser.add_argument(
        "--interval",
        type=int
    )

    parser.add_argument(
        "--time",
        default="15:33"
    )

    args = parser.parse_args()

    if not (
        args.run_once
        or args.scheduler
        or args.dashboard
    ):
        show_dashboard()
        return

    if args.dashboard:
        show_dashboard()

    if args.run_once:
        run_job()

    if args.scheduler:
        start_scheduler(
            run_job,
            interval_minutes=args.interval,
            daily_time=args.time
        )


if __name__ == "__main__":
    main()