from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchFrameException

#controlador que permite a selenium interactuar con el navegador Chrome
CHROMEDRIVER_PATH = './tests/drivers/chromedriver.exe'

def test_streamlit_app():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(CHROMEDRIVER_PATH)
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Navegador Chrome iniciado.")

        driver.get("https://ephanalysisdata.streamlit.app/")
        print("URL abierta.")

        # busca el iframe que contiene la aplicación Streamlit
        app_iframe = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='streamlitApp']"))
        )
        print("Iframe de la aplicación encontrado.")
        
        # Cambiar al contexto del iframe,("selenium entra al iframe") es decir, las siguientes operaciones de busqueda se haran en el iframe encontrado 
        driver.switch_to.frame(app_iframe)
        print("Contexto cambiado al iframe.")

        #espera 60 segs para q un elemento con el texto esperado sea visible en el iframe
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Encuest.AR') or contains(text(), 'Encuesta Permanente')]"))
        )
        #si coincide con el texto esperado, imprime un mensaje de éxito        
        if "Encuest.AR" in driver.page_source or "Encuesta Permanente" in driver.page_source:
            print("Texto esperado encontrado en la pagina.")
            print("\n¡La pagina se ha cargado correctamente y contiene el texto esperado!")
        else:
            raise TimeoutException("El texto esperado no fue encontrado en el page_source del iframe.")
    #posible exceso de tiempo de espera
    except TimeoutException:
        print("\n--- ERROR: TimeoutException ---")
        print("La página no se ha cargado correctamente o el texto esperado no está presente dentro del tiempo límite.")
        
        #si entra al error, imprime el contenido del iframe para debuggging 
        try:
            current_page_source = driver.page_source
            print("\nContenido del iframe (para depuración):\n")
            print(current_page_source.encode('utf-8', 'ignore').decode('utf-8'))
        except Exception:
            print("No se pudo obtener el page_source en este momento.")
        
        try:
            driver.switch_to.default_content()
        except NoSuchFrameException:
            pass

        raise

    except Exception as e:
        print(f"\n--- ERROR INESPERADO: {type(e).__name__} ---")
        print(f"Ocurrió un error inesperado: {e}")
        raise

    finally:
        if driver:
            print("\nCerrando el navegador.")
            driver.quit()

if __name__ == "__main__":
    test_streamlit_app()
