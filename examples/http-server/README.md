# pi-captcha HTTP Example

This is an HTTP server example project located at `pi-captcha/examples/http-server`, which makes it convenient to directly test and develop the `py_captcha` library within the repository.


## Download the font file
The font file size exceeds the limit. Please download the required fonts from https://github.com/wenlng/go-captcha-resources/tree/master/sourcedata/fonts and move them to `assets/fonts/` directory.

## Install Dependencies

It is recommended to create a virtual environment separately in the example directory:

```bash
cd examples/http-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Server

You can run the server from either the repository root directory or the example directory.

### Method 1: Run from the example directory

```bash
cd examples/http-server
source .venv/bin/activate
python app.py
```

### Method 2: Run from the repository root directory

```bash
cd /path/to/pi-captcha
python examples/http-server/app.py
```

The server will start at `http://localhost:5000`.

After starting, you can directly access:

- `http://localhost:5000/`
- `http://localhost:5000/web/`

## API Endpoints

### Generate Click Captcha
- **POST** `/api/captcha/click`
- Returns: Captcha ID, main image, thumbnail

### Generate Slide Captcha
- **POST** `/api/captcha/slide`
- Returns: Captcha ID, main image, puzzle piece

### Generate Rotate Captcha
- **POST** `/api/captcha/rotate`
- Returns: Captcha ID, main image, thumbnail

### Verify Captcha
- **POST** `/api/captcha/verify`
- Request body:
  ```json
  {
    "id": "captcha_id",
    "data": {
      // The data structure varies depending on the captcha type
    }
  }
  ```

## Notes

1. In production applications, you should use Redis or similar storage for captcha data
2. Example resources are located in the `assets/` directory of the current directory
3. The frontend needs to implement real user interaction logic