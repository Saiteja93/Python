
default_tags = {
    "environment" : "production",
    "owner" : "finance"
}

merge_tags = {

}

if merge_tags:
    print("it have elements")
else:
    print("none")


for tags in default_tags.items():
    key, value = tags
    print(f" {key} : {value}")


servers = ["web", "db", "backend"]

upper = [server.upper() for server in servers]
print(upper)


def user_name(name):
    print(f"my name is {name}")

user_name("teja")

def greeting(name):
    for names in name:
        print(f"hello {names}")


greeting(["sai", "Himu", "minni"])

def sum_numbers(number):
    return sum(x for x in number if x % 2 == 0)

print(sum_numbers([1,2,3,4,5,6,7,8]))

