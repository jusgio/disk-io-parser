import typer


app = typer.Typer()

@app.command()
def say_hello():
    print("Hello World")
