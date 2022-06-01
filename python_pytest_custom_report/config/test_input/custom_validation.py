import xml.etree.ElementTree as ET


def parse_xml(xmlfile):

    tree = ET.parse(xmlfile)

    root = tree.getroot()

    tests = []

    for testsuites_element in root:
        for testsuite_element in testsuites_element:

            test = {"name": testsuite_element.attrib["name"], "result": True}

            for child in testsuite_element:
                if child.tag == "failure":
                    test["result"] = False

            tests.append(test)

    return tests


def test_result(tests):
    test_num = 0
    print("Tests")
    print("-" * 40)
    for test in tests:
        test_num += 1
        pass_fail = "PASS" if test["result"] else "FAIL"
        print("{}. {}   {}".format(test_num, pass_fail, test["name"]))


def main():
    tests = parse_xml("pytest_results.xml")
    test_result(tests)


if __name__ == "__main__":
    main()
