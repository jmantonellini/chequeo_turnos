import warnings
import telegram
import asyncio
from playwright.async_api import async_playwright

# Ignorar advertencias de urllib3
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

TELEGRAM_CHANNEL_ID = "-1002337504567"
TELEGRAM_TOKEN = "7393396454:AAHO7wrC-cvZXksPVJxyPMXMrApUAdYe8sw"

bot = telegram.Bot(token=TELEGRAM_TOKEN)


async def send_telegram_message(message="Hello, World!"):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        print("Mensaje enviado con éxito.")
    except Exception as e:
        print("Error al enviar el mensaje de Telegram:", e)


async def automate_workflow():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(
            headless=False
        )  # Use headless=True for headless mode
        context = await browser.new_context()
        page = await context.new_page()

        # Step 1: Navigate to the page
        await page.goto(
            "https://www.exteriores.gob.es/Consulados/cordoba/es/Comunicacion/Noticias/Paginas/Articulos/Instrucciones-para-solicitar-cita-previa-para-LMD.aspx"
        )  # Replace with the actual page URL

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
        await page.wait_for_timeout(
            3000
        )  # Wait for 3 seconds to ensure the next page loads

        # Step 5: Click the green "Continuar / Continue" button
        continuar_locator = page.locator("button", has_text="Continuar")
        await continuar_locator.click()

        # Step 6: Wait for a few seconds to allow the API call to complete
        await page.wait_for_timeout(30000)

        # Step 7: Print the AllowAppointments property
        mensaje_locator = page.locator(
            "div#idDivBktServicesContainer", has_text="No hay horas"
        )
        if await mensaje_locator.is_visible():
            print("No hay horas disponibles.")
            await send_telegram_message("No hay horas, intentaré luego.")
        else:
            await send_telegram_message("FIJATE AHORA!! HAY TURNOS DISPONIBLES!!")
            await send_telegram_message("FIJATE AHORA!! HAY TURNOS DISPONIBLES!!")

        # Close the browser
        await browser.close()


# Run the function
asyncio.run(automate_workflow())
