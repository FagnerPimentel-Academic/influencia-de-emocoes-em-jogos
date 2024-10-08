using System.Collections;
using System.Collections.Generic;
using JetBrains.Annotations;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed;
    public float jumpForce;
    public int maxJumps = 2;

    private bool isGrounded = true;
    public int jumps = 0;
    public bool canJump = true;
    public float jumpCooldownTime = 1;
    public float lastTimeOnGround;

    Dictionary <string, Color> emotionPerColor = new Dictionary<string, Color>();

    private SpriteRenderer spriteRenderer;
    private Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        rb2d = GetComponent<Rigidbody2D>();
        lastTimeOnGround = Time.time;

        emotionPerColor.Add("NEUTRAL", Color.white);
        emotionPerColor.Add("HAPPY", Color.green);
        emotionPerColor.Add("SAD", Color.blue);
        emotionPerColor.Add("ANGRY", Color.red);
        emotionPerColor.Add("SCARY", Color.yellow);
    }

    // Update is called once per frame
    void Update()
    {
        Movement();
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.collider.CompareTag("Ground"))
        {
            isGrounded = true;
            lastTimeOnGround = Time.time;
        }
    }

    private void OnCollisionExit2D(Collision2D collision)
    {
        if (collision.collider.CompareTag("Ground"))
        {
            isGrounded = false;
        }
    }

    public void ApplyEmotion(string emotion){
        spriteRenderer.color = emotionPerColor[emotion];
    }

    private void Movement(){
        if(rb2d.velocity.y != 0 || jumps >= maxJumps)
            canJump = false;
        if(Time.time - lastTimeOnGround >= jumpCooldownTime && jumps < maxJumps){
            canJump = true;
            jumps=0;
        }
        

        var hDirection = Input.GetAxisRaw("Horizontal");
        var vDirection = Input.GetAxisRaw("Vertical");
        var jumpPressed = Input.GetButtonDown("Jump");

        if (hDirection == 1f)
        {
            spriteRenderer.flipX = false;
            transform.position = new Vector2(
                transform.position.x + speed * Time.deltaTime,
                transform.position.y
            );
        }
        else if (hDirection == -1f)
        {
            spriteRenderer.flipX = true;
            transform.position = new Vector2(
                transform.position.x - speed * Time.deltaTime,
                transform.position.y
            );
        }

        if (vDirection == 1f) { }
        else if (vDirection == -1f) { }

        if (jumpPressed)
        {
            if (canJump)
            {
                rb2d.velocity = new Vector2(rb2d.velocity.x, 0);
                rb2d.AddForce(new Vector2(0, jumpForce), ForceMode2D.Impulse);
            }

            jumps++;
        }

    }

    public bool GetIsGrounded(){
        return isGrounded;
    }

}
