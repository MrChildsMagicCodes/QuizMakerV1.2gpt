import xml.etree.ElementTree as ET
import zipfile
import os

def build_qti_zip(questions, zip_path):
    qti_root = ET.Element('questestinterop')
    assessment = ET.SubElement(qti_root, 'assessment', attrib={'title': 'Canvas Quiz', 'ident': 'quiz1'})
    section = ET.SubElement(assessment, 'section', attrib={'ident': 'root_section'})

    for idx, q in enumerate(questions):
        item = ET.SubElement(section, 'item', attrib={'ident': f'q{idx+1}', 'title': f'Question {idx+1}'})
        presentation = ET.SubElement(item, 'presentation')
        material = ET.SubElement(presentation, 'material')
        ET.SubElement(material, 'mattext').text = q['question']

        response_lid = ET.SubElement(presentation, 'response_lid', attrib={'ident': f'resp_{idx+1}', 'rcardinality': 'Single'})
        render_choice = ET.SubElement(response_lid, 'render_choice')

        for i, choice in enumerate(q['choices']):
            ident = chr(65 + i)
            label = ET.SubElement(render_choice, 'response_label', {'ident': ident})
            mat = ET.SubElement(label, 'material')
            ET.SubElement(mat, 'mattext').text = choice

        resproc = ET.SubElement(item, 'resprocessing')
        outcomes = ET.SubElement(resproc, 'outcomes')
        ET.SubElement(outcomes, 'decvar', {'vartype': 'Decimal', 'defaultval': '0', 'minvalue': '0', 'maxvalue': '100'})

        resp_condition = ET.SubElement(resproc, 'respcondition', {'continue': 'No'})
        conditionvar = ET.SubElement(resp_condition, 'conditionvar')
        ET.SubElement(conditionvar, 'varequal', {'respident': f'resp_{idx+1}'}).text = q['answer']
        setvar = ET.SubElement(resp_condition, 'setvar', {'action': 'Set'})
        setvar.text = '100'

    xml_path = zip_path.replace('.zip', '.xml')
    ET.ElementTree(qti_root).write(xml_path, encoding="utf-8", xml_declaration=True)

    manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="man1" xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
 xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1
 http://www.imsglobal.org/xsd/imscp_v1p1.xsd
 http://www.imsglobal.org/xsd/imsmd_v1p2
 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  <organizations/>
  <resources>
    <resource identifier="res1" type="imsqti_xmlv1p2" href="{os.path.basename(xml_path)}">
      <file href="{os.path.basename(xml_path)}"/>
    </resource>
  </resources>
</manifest>"""

    manifest_path = xml_path.replace(".xml", "_manifest.xml")
    with open(manifest_path, "w") as f:
        f.write(manifest)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(xml_path, arcname=os.path.basename(xml_path))
        zipf.write(manifest_path, arcname="imsmanifest.xml")
