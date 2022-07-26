import re
from collections import defaultdict
from typing import Dict, Iterable, List

from ultils import format_date, parse_url


class Collector(object):
    def __init__(
        self,
        key_range: Iterable[str],
        collect_point: Iterable[str],
        accepted_min_size: int,
        map_keys: dict,
    ):
        """
        A constructor function.

        :param key_range: the keys that are allowed to be collected
        :type key_range: Iterable[str]
        :param collect_point: The keys that will be used to determine if the data is ready to be collected
        :type collect_point: Iterable[str]
        :param accepted_min_size: The minimum number of items in the container before it is considered
        valid
        :type accepted_min_size: int
        :param map_keys: dict
        :type map_keys: dict
        """
        self.need_collect = False
        self.key_range = set(key_range)
        self.collect_point = set(collect_point)
        self.accepted_min_size = accepted_min_size
        self.map_keys = map_keys
        self.bundle = defaultdict(list)
        self.container: List[Dict] = []

    def before_update_bundle(self, key, label, text):
        """
        It takes the key, label, and text of the bundle, and returns the key and text.
        This function will be update key and text before it add to bundle by calling update_bundle

        :param key: The key of the bundle
        :param label: The label of the bundle
        :param text: The text that is currently in the text box
        :return: The key and text.
        """
        return key, text

    def update_bundle(self, label, text):
        """
        It takes a label and text, and then it updates the bundle with the text.

        The label is used to determine which key to use in the bundle.

        The text is used to update the bundle.

        The text is formatted before it is added to the bundle.  The text is formatted by calling the before_update_bundle function.

        The key and text are used to update the bundle.

        :param label: The label of the entity
        :param text: the text that is being processed
        :return: The key and text are being returned.
        """
        key = self.map_keys.get(label, "other")
        if label == "DATE":
            text = text.replace(".", "-")
            if text.count("-") == 1:
                startDate, endDate = text.split("-")
                if len(startDate) == len(endDate):
                    self.bundle["startDate"].append(startDate)
                    self.bundle["endDate"].append(endDate)
                    return
            text = format_date(text)
            if len(text) <= 1:
                return
        elif label == "URL":
            text = parse_url(text)
        elif label == "DOING":
            text = text[0].upper() + text[1:]
        key, text = self.before_update_bundle(key, label, text)

        self.bundle[key].append(text)

    def reset_bundle(self):
        self.bundle = defaultdict(list)

    def collect(self, entities):
        """
        It takes a list of entities (label, text) and appends them to a container as dictionary.

        The container is then appended to a list.

        The dictionary is reset after each valid append.

        :param entities: a list of tuples, each tuple is a pair of (label, text)
        """
        for label, text in entities:
            if self.check_collect_point(label):
                print(self.map_keys.get(label, "other") + " break to collect")
                self.container.append(self.bundle.copy())
                self.reset_bundle()
            self.update_bundle(label, text)
            debug_string = (
                f"bundle_size: {self.bundle_size} - bundle_keys: {self.bundle.keys()}"
            )
            print(debug_string)
            # print(self.bundle.values())

        if self.bundle_size >= self.accepted_min_size - 2:
            self.container.append(self.bundle.copy())
        else:
            if self.container:
                self.container[-1].update(self.bundle.copy())
        print(f"Done collected: {self.container}")
        self.reset_bundle()

    def get_main_keys(self, bundle):
        return set(filter(lambda x: x in self.collect_point, bundle.keys()))

    def reduce_container(self):
        """
        It takes a list of dictionaries, and merges the dictionaries that have the same value for a
        certain key
        """
        merge_container = []
        i = 0
        while i < len(self.container):
            j = min(len(self.container) - 1, i + 1)
            x = self.container[i]
            y = self.container[j]

            if self.collect_point - self.get_main_keys(x) == self.get_main_keys(y):
                z = self.merge_bundle(x, y)
                i += 2
                merge_container.append(z)
            else:
                i += 1
                merge_container.append(x)
        self.container = merge_container

    def merge_bundle(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    def get_container(self, except_key=None, select_type="min") -> Dict:
        """
        Get all the containers that the collector has been collected.

        :param except_key: a list of keys that you want to keep the list of values for
        :param select_type: "min" or "max", defaults to min (optional)
        :return: A list of dictionaries.
        """
        self.reduce_container()
        if except_key is None:
            except_key = {"other"}
        else:
            except_key = set(except_key)
            except_key |= {"other"}
        if select_type == "min":
            for bundle in self.container:
                for key, value in bundle.items():
                    if except_key and key in except_key:
                        if isinstance(value, Iterable):
                            try:
                                bundle[key] = list(dict.fromkeys(value))
                            except:
                                bundle[key] = value
                            continue
                    if isinstance(value, Iterable):
                        try:
                            bundle[key] = min(value)
                        except:
                            bundle[key] = value
                    else:
                        bundle[key] = value

        final_container = []
        for bundle in self.container:
            if len(bundle) > 1:
                final_container.append(bundle.copy())
        self.container = final_container
        return self.container

    @property
    def is_full_bundle(self):
        return self.bundle.keys() == self.key_range

    @property
    def bundle_size(self):
        return self.size_bundle(self.bundle)

    def size_bundle(self, bundle):
        keys = []
        for key in bundle:
            if key not in ["highlights", "other", "keywords", "url", "unlabeled"]:
                keys.append(key)

        return len(keys)

    def check_collect_point(self, label):
        """
        Check if current entity is collector point for collector compresses a container

        :param label: the label of the current point
        :return: a boolean value. true if current entity is a collector point
        """
        key = self.map_keys.get(label, "other")
        if key not in self.collect_point:
            return False
        if key not in self.bundle.keys():
            return False

        return self.bundle_size >= self.accepted_min_size
