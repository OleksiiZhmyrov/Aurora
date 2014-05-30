class Stats(object):
    def __init__(self, issues):
        self.issues = issues

    def __get_ready(self):
        count = len([issue for issue in self.issues if issue.dc_status == 'READY'])
        count_sp = sum([int(issue.get_custom_field('points')) for issue in self.issues if
                        issue.get_custom_field('points') != '' and issue.dc_status == 'READY'])
        percent = round(100.0 * count / int(self.__get_total()['count']), 0)
        percent_sp = round(100.0 * count_sp / int(self.__get_total()['count_sp']), 0)
        return self.__get_result_node(count, count_sp, percent, percent_sp)

    def __get_passed(self):
        count = len([issue for issue in self.issues if issue.dc_status == 'PASS'])
        count_sp = sum([int(issue.get_custom_field('points')) for issue in self.issues if
                        issue.get_custom_field('points') != '' and issue.dc_status == 'PASS'])
        percent = round(100.0 * count / int(self.__get_total()['count']), 0)
        percent_sp = round(100.0 * count_sp / int(self.__get_total()['count_sp']), 0)
        return self.__get_result_node(count, count_sp, percent, percent_sp)

    def __get_failed(self):
        count = len([issue for issue in self.issues if issue.dc_status == 'FAIL'])
        count_sp = sum([int(issue.get_custom_field('points')) for issue in self.issues if
                        issue.get_custom_field('points') != '' and issue.dc_status == 'FAIL'])
        percent = round(100.0 * count / int(self.__get_total()['count']), 0)
        percent_sp = round(100.0 * count_sp / int(self.__get_total()['count_sp']), 0)
        return self.__get_result_node(count, count_sp, percent, percent_sp)

    def __get_other(self):
        count = len([issue for issue in self.issues if issue.dc_status == ''])
        count_sp = sum([int(issue.get_custom_field('points')) for issue in self.issues if
                        issue.get_custom_field('points') != '' and issue.dc_status == ''])
        percent = round(100.0 * count / int(self.__get_total()['count']), 0)
        percent_sp = round(100.0 * count_sp / int(self.__get_total()['count_sp']), 0)
        return self.__get_result_node(count, count_sp, percent, percent_sp)

    def __get_progress_bar(self):
        return {
            'passed': int(self.__get_passed()['percent']),
            'ready': int(self.__get_ready()['percent']),
            'other': int(self.__get_failed()['percent'] + self.__get_other()['percent'])
        }

    def __get_total(self):
        return {
            'count': len(self.issues),
            'count_sp': sum(
                int(issue.get_custom_field('points')) for issue in self.issues if issue.get_custom_field('points') != '')
        }

    @staticmethod
    def __get_result_node(count, count_sp, percent, percent_sp):
        return {
            'count': int(count),
            'count_sp': int(count_sp),
            'percent': int(percent),
            'percent_sp': int(percent_sp),
        }

    def get_result(self):
        return {
            'datetime': None,
            'ready': self.__get_ready(),
            'total': self.__get_total(),
            'passed': self.__get_passed(),
            'failed': self.__get_failed(),
            'other': self.__get_other(),
            'progressbar': self.__get_progress_bar(),
        }

