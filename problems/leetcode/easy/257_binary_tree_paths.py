# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binary_tree_paths(self, root: TreeNode) -> list[str]:
      def dfs(curr_node: TreeNode, node_vals: list[int], tree_paths: list[str]) -> None:
        if curr_node is None:
          return

        node_vals.append(curr_node.val)

        if curr_node.left is None and curr_node.right is None:
          tree_paths.append('->'.join(map(str, node_vals)))
          node_vals.pop()
          return

        dfs(curr_node.left, node_vals, tree_paths)
        dfs(curr_node.right, node_vals, tree_paths)

        node_vals.pop()


      result = list()
      dfs(root, [], result)
      return result


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)

    result = Solution().binary_tree_paths(root)
    assert len(result) == 2
    assert '1->2->5' in result
    assert '1->3' in result




