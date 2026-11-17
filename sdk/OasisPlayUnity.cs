using System;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Networking;

namespace Oasis.PlaySDK
{
    public class OasisClient : MonoBehaviour
    {
        public string gatewayUrl = "http://127.0.0.1:8080";

        [Serializable]
        public class JobPayload
        {
            public string skill = "play";
            public string prompt;
        }

        public async Task<string> OffloadComputeAsync(string jobSpec)
        {
            var payload = JsonUtility.ToJson(new JobPayload { prompt = jobSpec });
            using (var request = new UnityWebRequest(gatewayUrl + "/v1/skill", "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(payload);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");

                var operation = request.SendWebRequest();
                while (!operation.isDone) await Task.Yield();

                return request.result == UnityWebRequest.Result.Success
                    ? request.downloadHandler.text
                    : "{\"error\":\"" + request.error + "\"}";
            }
        }
    }
}
