import glob
import os
import re
import sys


DEPT_DISPLAY_BY_ID = {
    "00_Distrito_Capital": "Distrito Capital",
    "01_Concepcion": "Concepción",
    "02_San_Pedro": "San Pedro",
    "03_Cordillera": "Cordillera",
    "04_Guaira": "Guaira",
    "05_Caaguazu": "Caaguazu",
    "06_Caazapa": "Caazapa",
    "07_Itapua": "Itapua",
    "08_Misiones": "Misiones",
    "09_Paraguari": "Paraguari",
    "10_Alto_Parana": "Alto Parana",
    "11_Central": "Central",
    "12_Neembucu": "Neembucu",
    "13_Amambay": "Amambay",
    "14_Canindeyu": "Canindeyu",
    "15_Presidente_Hayes": "Presidente Hayes",
    "16_Boqueron": "Boqueron",
    "17_Alto_Paraguay": "Alto Paraguay",
}


def build_district_index():
    index = {}
    base_dir = "Departamentos"

    for dept_dir in sorted(glob.glob(os.path.join(base_dir, "*"))):
        if not os.path.isdir(dept_dir):
            continue

        dept_id = os.path.basename(dept_dir)
        dept_display = DEPT_DISPLAY_BY_ID.get(dept_id, dept_id.split("_", 1)[-1].replace("_", " "))

        for district_dir in sorted(glob.glob(os.path.join(dept_dir, "*"))):
            if not os.path.isdir(district_dir):
                continue

            raw_dist_name = os.path.basename(district_dir)
            district_name = raw_dist_name.replace("_", " ")
            label = f"dist:{dept_id}:{raw_dist_name}"
            index.setdefault(district_name, []).append((dept_display, label))

    return index


def replace_links(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    district_index = build_district_index()
    if not district_index:
        raise RuntimeError("Nao foi possivel construir o indice de distritos para links.")

    def replacement(match, dept_display=None):
        district_name = match.group(1)
        display_name = match.group(2)
        entry = district_index.get(district_name)
        if not entry:
            return match.group(0)

        if len(entry) == 1:
            return f"\\hyperref[{entry[0][1]}]{{{display_name}}}"

        # Desambigua pelo departamento mostrado na mesma linha.
        if dept_display:
            for known_dept, label in entry:
                if known_dept == dept_display:
                    return f"\\hyperref[{label}]{{{display_name}}}"

        return f"\\hyperref[{entry[0][1]}]{{{display_name}}}"

    line_pattern = re.compile(r"\\hyperref\[dist:([^\]]+)\]\{([^}]+)\}")
    lines = []
    for line in content.splitlines():
        if "\\hyperref[dist:" in line:
            dept_match = re.search(r"\\hyperref\[dept:([^\]]+)\]\{([^}]+)\}", line)
            dept_display = dept_match.group(2) if dept_match else None
            line = line_pattern.sub(lambda m: replacement(m, dept_display), line)
        lines.append(line)

    new_content = "\n".join(lines) + ("\n" if content.endswith("\n") else "")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        replace_links(sys.argv[1])
