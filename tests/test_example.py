def test_example(page):
    page.goto("https://dummypay.vercel.app/")

    assert page.title() != ""