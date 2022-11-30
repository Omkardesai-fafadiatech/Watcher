# Queries

## Assignees of Older Issues (Open since Last 15 days)
    ```
        SELECT COUNT(*) as total, auth_user.username FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE core_issue.status='open' AND DATE(core_issue.created_at) < (CURRENT_DATE - 15) GROUP BY auth_user.username ORDER BY total DESC;
    ```

## Breakdown by Status
    ```
        SELECT COUNT(*) as total, status FROM core_issue GROUP BY status ORDER BY total DESC;
    ```

## Breakdown by Status (Last 15 Days)
    ```
        SELECT COUNT(*) as total, status FROM core_issue WHERE DATE(created_at) > (CURRENT_DATE - 15) GROUP BY status ORDER by total DESC;
    ```

## Breakdown of Issues by Users
    ```
        SELECT auth_user.username, core_issue.status, COUNT(*) as total FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE auth_user.id NOT IN (6, 12) GROUP BY auth_user.username, core_issue.status;
    ```

## Breakdown of Issues by Users (Last 15 Days)
    ```
        SELECT auth_user.username, core_issue.status, COUNT(*) as total FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE auth_user.id NOT IN (6, 12) AND DATE(core_issue.created_at) > (CURRENT_DATE - 15) GROUP BY auth_user.username, core_issue.status;
    ```

## Closed issues by Users (Last 7 Days)
    ```
        SELECT COUNT(*) as total, auth_user.username FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE core_issue.status = 'closed' AND DATE(closed_on) >= (CURRENT_DATE -7) GROUP BY auth_user.username ORDER BY total DESC;
    ```

## Issues Closed (Last 15 days)
    ```
        SELECT COUNT(*), DATE(closed_on)FROM core_issue WHERE DATE(closed_on) > (CURRENT_DATE - 15) GROUP BY DATE(closed_on) ORDER BY DATE(closed_on) DESC;
    ```

## Issues opened (Last 60 days)
    ```
        SELECT COUNT(*), DATE(created_at)FROM core_issue WHERE DATE(created_at) > (CURRENT_DATE - 60) GROUP BY DATE(created_at) ORDER BY DATE(created_at) DESC;
    ```

## Oldest Issues
    ```
        SELECT DATE(core_issue.created_at), core_issue.issue_number, auth_user.username, core_issue.title FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE status = 'open' ORDER BY core_issue.created_at LIMIT 50;
    ```

## Open Issues by Users
    ```
        SELECT COUNT(*) as total, auth_user.username FROM core_issue JOIN auth_user ON core_issue.assignee_id = auth_user.id WHERE core_issue.status = 'open' GROUP BY auth_user.username ORDER BY total DESC;
    ```