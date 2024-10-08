using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public Transform player;
    public new Camera camera;
    public float yOffset = 3.85f;
    public float followSpeed = 0.1f;
    public float closeSpeed = 0.01f;
    public float normalSize = 5;
    public float closeSize = 4;
    public bool close = false;

    private float currentSize;

    [HideInInspector] public static CameraController instance;

    void Start(){
        instance = this;
        currentSize = camera.orthographicSize;
    }

    void FixedUpdate(){
        var pos = player.position;
        pos.y += yOffset * currentSize/normalSize;

        transform.position = Vector2.Lerp(transform.position, pos, followSpeed);

        if(close && currentSize != closeSize){
            currentSize = camera.orthographicSize;
            camera.orthographicSize = Mathf.Lerp(currentSize, closeSize, closeSpeed);
        }else if(!close && camera.orthographicSize != normalSize){
            currentSize = camera.orthographicSize;
            camera.orthographicSize = Mathf.Lerp(currentSize, normalSize, closeSpeed);
        }
    }

    void Update(){
        
    }
}
