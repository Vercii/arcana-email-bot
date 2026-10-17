const data = $("Edit Fields1").first().json;

const parts = (data.callback_data || "").split(":");

const action = parts[0];
const request_id = parts.slice(1).join(":");

const valid_callback =
  (action === "approve" || action === "cancel") &&
  request_id.length > 0;

return {
  json: {
    action: valid_callback ? action : null,
    request_id: valid_callback ? request_id : null,
    valid_callback,
    telegram_user_id: data.telegram_user_id,
    chat_id: data.chat_id,
    callback_query_id: data.callback_query_id
  }
};
