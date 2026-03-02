def find_paris(nums, target):
    ans = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                ans.append([i, j])
    return ans[0] if len(ans) == 1 else ans if ans else -1

