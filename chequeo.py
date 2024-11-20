import warnings
import telegram
import random
import asyncio
import time
from playwright.async_api import async_playwright

# Ignorar advertencias de urllib3
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

TELEGRAM_CHANNEL_ID = "-1002337504567"
TELEGRAM_CHAT_ID = "1579035548"
TELEGRAM_TOKEN = "7393396454:AAHO7wrC-cvZXksPVJxyPMXMrApUAdYe8sw"

bot = telegram.Bot(token=TELEGRAM_TOKEN)


async def send_channel_message(message="Hello, World!"):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        print("Mensaje enviado con éxito.")
    except Exception as e:
        print("Error al enviar el mensaje de Telegram:", e)


async def send_chat_message(message="Hello, World!"):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("Mensaje enviado con éxito.")
    except Exception as e:
        print("Error al enviar el mensaje de Telegram:", e)


async def send_telegram_photo(photo_path):
    try:
        with open(photo_path, "rb") as photo:
            await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=photo)
        print("Foto enviada con éxito.")
    except Exception as e:
        print("Error al enviar la foto de Telegram:", e)


async def automate_workflow():
    sleep_time = random.randint(
        0, 300
    )  # Random sleep time between 0 and 300 seconds (0 to 5 minutes)
    print(f"Sleeping for {sleep_time} seconds to avoid detection...")
    time.sleep(sleep_time)

    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(
            headless=True
        )
        context = await browser.new_context()
        page = await context.new_page()

        # Step 1: Navigate to the page
        await page.goto(
            "https://www.exteriores.gob.es/Consulados/cordoba/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa-para-LMD.aspx"
        )

        await page.wait_for_timeout(3000)

        await page.evaluate("window.scrollTo(0, 2231)")

        await page.wait_for_timeout(2000)

        # Step 2: Click the "AQUÍ" link
        aqui_locator = page.locator("a", has_text="AQUÍ. ")
        if await aqui_locator.is_visible():
            print("The 'AQUÍ' link is visible. Clicking now...")
            await aqui_locator.click()
        else:
            print("The 'AQUÍ' link is not visible on screen.")
            await browser.close()
            return

        # Step 3: Handle the Chrome dialog
        page.on("dialog", lambda dialog: dialog.accept())  # Automatically click "OK"

        # Step 4: Wait for a few seconds after clicking the dialog
        print("Esperando 3 segundos...")
        await page.wait_for_timeout(
            3000
        )  # Wait for 3 seconds to ensure the next page loads

        # Step 5: Click the green "Continuar / Continue" button
        continuar_locator = page.locator("button", has_text="Continuar")
        print("Clickeando el botón 'Continuar'...")
        await continuar_locator.click()

        # Step 6: Wait for a few seconds to allow the API call to complete
        print("Esperando 30 segundos...")
        await page.wait_for_timeout(30000)

        # Step 7: Print the AllowAppointments property
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Chequeo hecho a las: ({current_time})")
        mensaje_locator = page.locator(
            "div#idDivBktServicesContainer", has_text="No hay horas"
        )
        if await mensaje_locator.is_visible():
            print("No hay horas disponibles.")
            await send_chat_message(
                f"No hay horas, intentaré luego. Chequeo hecho a las: ({current_time})"
            )
        else:
            screenshot_path = "screenshot.png"
            await page.screenshot(path=screenshot_path)
            await send_telegram_photo(screenshot_path)
            await send_channel_message(
                "FIJATE AHORA!! HAY TURNOS DISPONIBLES!! Chequeo hecho a las: ({current_time})"
            )

        # Close the browser
        await browser.close()


# Run the function
asyncio.run(automate_workflow())
