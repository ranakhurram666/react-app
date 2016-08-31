from server import app

if __name__ == '__main__':
    app.run()
    app.debug = True


@app.teardown_appcontext
def close_db():
    """
    Close database at end of app context.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()