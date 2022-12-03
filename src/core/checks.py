import re

def is_emoji(content:str):
    regexp = u'[\u2600-\u26FF]|[\u2700-\u27BF]|[\U0001f300-\U0001f5fF]|[\U0001f600-\U0001f64F]|[\U0001f680-\U0001f6FF]'
    result = re.findall(regexp, content, re.UNICODE)
    result += re.findall("<:\w+:\d+>|<\w+:\w+:\d+>",content) 

    return False if len(result) == 0 else True

def is_available_language(content:str):
    regexp = u"[\u4E00-\u9FFF]|[\uAC00-\uD7A3]|[\u3041-\u309f]|[\u0000-\u007F]"
    result = re.findall(regexp, content, re.UNICODE)
    
    return False if len(list(filter(lambda x:x not in result, content))) > 0 else True

if __name__ == "__main__":
    def test(data:str):
        result = []
        for i,d in enumerate(data.split()):
            result.append((d, ch:=is_available_language(d)))
            print(f"test{i+1}:", d, ch)

        return result

    print(test(input()))