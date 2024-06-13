link_bugs = {
    "broken_link": [
        '<a href="nonexistent.html">Broken Link</a>',
        '<a href="404.html">Another Broken Link</a>'
    ],
    "non_visible_link": [
        '<a href="https://n12.com" style="display:none;">Invisible Link</a>',
        '<a href="https://n12.com" style="visibility:hidden;">Another Invisible Link</a>'
    ],
    "no_href_link": [
        '<a>Link Without Href</a>',
        '<a href="">Empty Href Link</a>'
    ],
    "incorrect_anchor_link": [
        '<a href="#nonexistent_anchor">Broken Anchor</a>'
    ],
    "javascript_link": [
        '<a href="javascript:void(0);">JavaScript Link</a>'
    ]
}