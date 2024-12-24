def update_course_for_user(file_path, user_id, new_course_id):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    user_id_str = str(user_id)
    updated_lines = []
    user_found = False

    for line in lines:
        if line.startswith(user_id_str + ' '):
            updated_line = line.strip() + ' ' + str(new_course_id) + '\n'
            updated_lines.append(updated_line)
            user_found = True
        else:
            updated_lines.append(line)

    if not user_found:
        updated_lines.append(f"{user_id} {new_course_id}\n")

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

# Example usage
if __name__ == "__main__":
    file_path = '../data/test/train.txt'
    update_course_for_user(file_path, 1, 4119)
