def format_url(fileurl):
    tmpchr=""
    tmpchrs=""
    for chars in fileurl:
            if chars == '/':
                    tmpchr = ""
            else:
                    tmpchr+=chars
    for chars in tmpchr:
            if chars != '_':
                    tmpchrs+=chars
            else:
                    break
    return tmpchrs

print(format_url("a/b_c"))
print(format_url("a/a/b_c"))
