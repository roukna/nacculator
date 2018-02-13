import sys

import xml.etree.ElementTree as ET
import csv
import smtplib


def generate_report(filename):
    tree = ET.parse(filename)
    pages = tree.getroot()
    final_result = {}

    for iter in pages[0].findall('textbox'):
        # ADC IDs Total
        if iter.attrib['id'] == '36':
            result = []
            for t_iter in iter.findall('textline')[-1].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['ADC IDs Total'] = ''.join(result)

        # ADC Percentage
        if iter.attrib['id'] == '34':
            result = []
            for t_iter in iter.findall('textline')[-1].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['ADC Percentage'] = ''.join(result)

        # Autopsies
        if iter.attrib['id'] == '37':
            result = []
            for t_iter in iter.findall('textline')[0].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['Autopsies'] = ''.join(result)

        # Autopsies Percentage
        if iter.attrib['id'] == '35':
            result = []
            for t_iter in iter.findall('textline')[0].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['Autopsies Percentage'] = ''.join(result)

        # NP Forms
        if iter.attrib['id'] == '37':
            result = []
            for t_iter in iter.findall('textline')[1].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['NP Forms'] = ''.join(result)

        # 6+
        if iter.attrib['id'] == '9':
            result = []
            for t_iter in iter.findall('textline')[0].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['6+'] = ''.join(result)

        # <6
        if iter.attrib['id'] == '4':
            result = []
            for t_iter in iter.findall('textline')[0].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            final_result['<6'] = ''.join(result)

        # Date Entered
        if iter.attrib['id'] == '0':
            result = []
            for t_iter in iter.findall('textline')[0].findall('text'):
                if t_iter.text.strip():
                    result.append(t_iter.text)
            result = str.replace(''.join(result), 'Asof', '')
            final_result['Date Entered'] = result

        with open('report.csv', 'wb') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in final_result.items():
                writer.writerow([key, value])


def generate_xml(filename):
    pass


def main(argv):
    filename = argv
    # TODO generate_xml(filename), pass xml filename to generate_report
    generate_report(filename)


if __name__ == '__main__':
    main(sys.argv[1])
