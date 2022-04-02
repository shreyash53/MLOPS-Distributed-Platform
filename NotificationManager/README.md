# Notification Manager

## Files
1. `notificationmanager.py` - Web API for sending and fetching notifs.

## Endpoints exposed
### 1. /notify - ("POST")
**Requires :**  
* `recipient_id` - username of recipient  
* `msg` - message string  

**Returns :**
* `None`
### 2. /fetch - ("GET")
**Requires :**  
* `recipient_id` - username of recipient  

**Returns :**
* `List of notifications for recipient_id sorted by most recent`

## Data Structure
### 'Notification' Schema
* _id : auto
* recipient_id : Reference(Actor)
* msg : string
* is_read : bool

## Databases Accessed
1. **User database** - For recipient verification
2. **Notifications database** - For notification storage / retrieval.
