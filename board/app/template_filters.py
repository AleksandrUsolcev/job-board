from app import app


@app.template_filter(name='brline')
def brline_filter(text):
    return text.replace('\n', '<br>')
