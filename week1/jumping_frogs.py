visited = []
leaves = []


def makeInitialPosition(n_frogs=2):
    return 'L' * n_frogs + '_' + 'R' * n_frogs


def swap(text, ch1, ch2):
    text = text.replace(ch2, '!',)
    text = text.replace(ch1, ch2)
    text = text.replace('!', ch1)
    return text


def generateChildren(steppp):
    result = []
    index = 0
    for el in steppp:

        newStep = steppp
        newStep = newStep.replace('_', el)
        newStepList = list(newStep)
        newStepList[index] = '_'
        newStep = ''.join(newStepList)

        # check is valid and append
        valid = True
        if ((el == 'L') & (index > newStep.find('_'))):  # move only in right
            valid = False

        if ((el == 'R') & (index < newStep.find('_'))):  # move only in left
            valid = False

        if ((el == 'R') & (steppp.index('_') > index)):  # LLRR_ =>/ LLR_R
            valid = False

        if ((el == 'L') & (steppp.index('_') < index)):  # RR_LL =>/ RRLL_
            valid = False

        step_index = steppp.find("_")
        new_step_index = newStep.find("_")

        if abs(new_step_index - step_index) >= 3:  # more than 1 step
            valid = False

        if valid:
            result.append(newStep)
        index += 1

    result.remove(steppp)

    return result


def is_not_traveresed(step):
    return step not in visited


def check_children(children):
    return any([child not in visited for child in children])


def markAsLeaf(step):
    leaves.append(step)


def dfs(graph, root):
    children = generateChildren(root)
    graph[root] = children

    asd = set(graph[root]) - set(visited) - set(leaves)
    for child in sorted(asd):
        if 'RR_LL' in visited:
            return visited
        if child == 'RR_LL':
            visited.append(root)
            visited.append(child)
            return visited

        children = generateChildren(child)
        has_valid_children = check_children(children)

        if not has_valid_children:
            markAsLeaf(child)
            markAsLeaf(root)
            dfs(graph, root)

        if has_valid_children:
            visited.append(root)
            dfs(graph, child)

    return visited


def frogs():
    initial_root = makeInitialPosition()
    initial_graph = {initial_root: set([])}

    result = dfs(initial_graph, initial_root)

    dfs_result = []
    for el in result:
        if el not in dfs_result:
            dfs_result.append(el)
    print(dfs_result)


if __name__ == "__main__":
    frogs()