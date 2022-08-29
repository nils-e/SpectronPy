# result.py

import dataclasses

import selenium.webdriver.support.expected_conditions as Expected
from selenium.webdriver.remote.webelement import WebElement

import lib.expected as SpectronExpected


@dataclasses.dataclass
class Result:
    result: dict
    summary: bool = False


class ResultDict(dict):
    def add(self, result: Result):
        self.update(result.result)

    def summarize_all(self):
        return all([v for k, v in self.items()])

    def summarize_any(self):
        return any([v for k, v in self.items()])


def _verify_match(element: WebElement, kwargs) -> ResultDict:
    results_list = ResultDict()
    driver = element.parent

    if kwargs.get('visible', None):
        result = {'visible': bool(Expected.visibility_of(element)(None))}
        results_list.add(Result(result))

    if option := kwargs.get('text', None):
        result = {'text': SpectronExpected.text_to_be_present_in_element(element, option)(driver)}
        results_list.add(Result(result))

    return results_list


def _generate_results(results: list | dict, result: dict, summarize=False) -> list | dict:
    if summarize:
        rtn = next(iter(result.values()))
        results.append(rtn)
    else:
        results.update(result)

    print(results)
    return results
