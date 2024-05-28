from decimal import Decimal
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

def process_payments():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port = 3307,
            user="root",
            password="S3cR3tUs3R",
            database="desktopdb"
        )
        cursor = db.cursor()

        # Get all active Susu groups and their intervals
        cursor.execute("SELECT Group_ID, Contribution_Interval, Contribution_Amount FROM susu_groups WHERE status = 'Active'")
        groups = cursor.fetchall()

        for group_id, contirbution_interval, contribution_amount in groups:
            interval_days = int(contirbution_interval)
            contribution_amount = Decimal(contribution_amount)
            
            # Get the members of the group
            cursor.execute("SELECT member_id, Email FROM susu_members WHERE group_id = %s ORDER BY joined_at", (group_id,))
            members = cursor.fetchall()
            
            # Calculate the next payment date for the group
            cursor.execute("SELECT start_date FROM susu_groups WHERE Group_ID = %s", (group_id,))
            start_date = cursor.fetchone()[0]
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

            days_since_start = (datetime.now() - start_date).days
            next_payment_index = (days_since_start // interval_days) % len(members)
            next_payment_member = members[next_payment_index]

            # Check if the total contributions for the current interval meet the required amount
            expected_total = len(members) * contribution_amount
            interval_start_date = start_date + timedelta(days=(days_since_start // interval_days) * interval_days)
            interval_end_date = start_date + timedelta(days=((days_since_start // interval_days) + 1) * interval_days)
            cursor.execute("SELECT SUM(amount) FROM contributions WHERE group_id = %s AND Contribution_date BETWEEN %s AND %s", 
                           (group_id, start_date + timedelta(days=(days_since_start // interval_days) * interval_days), 
                            start_date + timedelta(days=((days_since_start // interval_days) + 1) * interval_days)))
            total_contributed = cursor.fetchone()[0]

            if total_contributed is None or total_contributed < expected_total:
                logging.info(f"Total contributions for group {group_id} do not meet the expected amount. Skipping payment.")
                continue

             # Ensure the group has enough funds
            cursor.execute("SELECT total_funds FROM group_funds WHERE group_id = %s", (group_id,))
            group_funds = cursor.fetchone()
            if  group_funds is None or group_funds[0] < expected_total:
                logging.info(f"Group {group_id} does not have enough funds. Skipping payment.")
                continue

            # Make the payment to the member
            member_id, email = next_payment_member
            amount = expected_total  # Total amount to be paid to the member

            cursor.execute("UPDATE susu_account SET Balance = Balance + %s WHERE member_id = %s", (amount, member_id))
            db.commit()

            #deduct the paid amount from the group's total funds
            cursor.execute("UPDATE group_funds SET total_funds = total_funds - %s WHERE group_id = %s", (amount, group_id))
            db.commit()

            # Send notification
            message = f"You have received your Susu payment of {amount}."
            cursor.execute("INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)", (message, email))
            db.commit()

            # Reset contributions for the next cycle
            cursor.execute("UPDATE contributions SET amount = 0.00 WHERE group_id = %s", (group_id,))
            db.commit()

        cursor.close()
        db.close()
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_payments, 'interval', days=1)
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
    while True:
        pass  # Keep the script running
