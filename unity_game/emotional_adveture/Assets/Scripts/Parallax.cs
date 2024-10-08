using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Parallax : MonoBehaviour
{
    private new Transform camera;
    private Vector3 startPos;

    public float parallaxEffect;
    // Start is called before the first frame update
    void Start()
    {
        camera = Camera.main.transform;
        startPos = transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        var distance = camera.transform.position;
        transform.position = new Vector2(startPos.x + distance.x * parallaxEffect, startPos.y + distance.y * parallaxEffect);
    }
}
