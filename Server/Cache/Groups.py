from Group import GroupUtils

groups_data = {}


def getGroupsId():
    return ['12345']


def initGroups():
    for i in getGroupsId():
        groups_data[i] = GroupUtils.GroupData(i)


def getGroupData(group_id):
    if group_id in groups_data.keys():
        return groups_data[group_id]
    else:
        return None


def setGroup(group_id, group_data):
    groups_data[group_id] = group_data


def delGroup(group_id):
    if group_id in groups_data.keys():
        del groups_data[group_id]
