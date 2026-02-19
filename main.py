from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Sexy World"}


def main():
    print("Hello from fastapi-tutorial!")


if __name__ == "__main__":
    main()
