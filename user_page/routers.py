import user_page.view as view

router: dict = {
    '': view.UserPage(),
    '2/': view.user_page2
}
