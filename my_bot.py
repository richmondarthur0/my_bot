import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Replace YOUR_BOT_API_TOKEN with your bot's API token.
updater = Updater("6061696205:AAG2FCRawFOJ7wkbX13-8gZj3yhSRBikQ4s", use_context=True)
print("Starting bot...")  # Add this line to print a message when the script starts.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! What is your name?')

def basic_salary(update, context):
    """Ask the user for their basic salary."""
    name = update.message.text
    context.user_data['name'] = name
    update.message.reply_text(f'Okay {name}, what is your basic salary?')

def calculate_income(update, context):
    """Calculate the user's suggested net income."""
    basic_salary = float(update.message.text)
    weekdays_hours = float(context.user_data['weekdays_hours'])
    saturdays_hours = float(context.user_data['saturdays_hours'])
    sundays_holidays_hours = float(context.user_data['sundays_holidays_hours'])
    weekdays_income = (basic_salary / 30) * (1.25 * weekdays_hours / 8)
    saturdays_income = (basic_salary / 30) * (1.5 * saturdays_hours / 8)
    sundays_holidays_income = (basic_salary / 30) * (2 * sundays_holidays_hours / 8)
    total_income = weekdays_income + saturdays_income + sundays_holidays_income
    suggested_net_income = total_income / (2718.49 * 471.18)
    update.message.reply_text(f'Your suggested net income is {suggested_net_income:.2f}$.')

def weekdays_hours(update, context):
    """Ask the user for their weekdays hours."""
    weekdays_hours = update.message.text
    context.user_data['weekdays_hours'] = weekdays_hours
    update.message.reply_text('How many Saturdays hours did you make this month?')

def saturdays_hours(update, context):
    """Ask the user for their Saturdays hours."""
    saturdays_hours = update.message.text
    context.user_data['saturdays_hours'] = saturdays_hours
    update.message.reply_text('How many Sundays and Holiday hours did you make this month?')

def sundays_holidays_hours(update, context):
    """Ask the user for their Sundays and holidays hours."""
    sundays_holidays_hours = update.message.text
    context.user_data['sundays_holidays_hours'] = sundays_holidays_hours
    update.message.reply_text('Calculating your suggested net income...')
    calculate_income(update, context)

def main():
    """Start the bot."""
    # Replace YOUR_BOT_API_TOKEN with your bot's API token.
    updater = Updater("6061696205:AAG2FCRawFOJ7wkbX13-8gZj3yhSRBikQ4s", use_context=True)

    # Get the dispatcher to register handlers.
    dp = updater.dispatcher

    # Add handlers for the /start and message commands.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(filters.text & (~filters.command), basic_salary))
    dp.add_handler(MessageHandler(filters.regex(r'^\d+(\.\d+)?$'), weekdays_hours))
    dp.add_handler(MessageHandler(filters.regex(r'^\d+(\.\d+)?$'), saturdays_hours))
    dp.add_handler(MessageHandler(filters.regex(r'^\d+(\.\d+)?$'), sundays_holidays_hours))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is exited
    updater.idle()