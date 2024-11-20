using System.Collections;
using System.Collections.Generic;
using JetBrains.Annotations;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    public float speed;
    public float jumpForce;
    public bool canJump = true;
    public float lastTimeOnGround;
    private bool isGrounded = true;
    private string emotion = "NEUTRAL";
    private int hp = 10;
    public bool isAlive = true;
    private bool animationLocked = false;

    Dictionary<string, Color> emotionPerColor = new Dictionary<string, Color>();

    private GameManager gameManager;
    private AnimationController animationController;
    private SpriteRenderer spriteRenderer;
    private Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.instance;
        spriteRenderer = GetComponent<SpriteRenderer>();
        rb2d = GetComponent<Rigidbody2D>();
        lastTimeOnGround = Time.time;
        animationController = GetComponent<AnimationController>();

        emotionPerColor.Add("NEUTRAL", Color.white);
        emotionPerColor.Add("HAPPY", Color.green);
        emotionPerColor.Add("SAD", Color.grey);
        emotionPerColor.Add("ANGRY", Color.red);
        emotionPerColor.Add("FEAR", Color.blue);
    }

    // Update is called once per frame
    void Update()
    {
        if (isAlive)
        {
            Movement();
            Attack();
        }
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

    public void ApplyEmotion(string emotion)
    {
        this.emotion = emotion;
    }

    private void Attack()
    {
        var attackPressed = Input.GetButtonDown("Attack");
        if (attackPressed)
            PlayAnimation("player_attack");
    }

    private void Movement()
    {
        if (rb2d.velocity.y != 0)
        {
            canJump = false;
        }
        else
        {
            canJump = true;
        }

        var hDirection = Input.GetAxisRaw("Horizontal");
        var vDirection = Input.GetAxisRaw("Vertical");
        var jumpPressed = Input.GetButtonDown("Jump");

        if (hDirection == 1f)
        {
            PlayAnimation("player_walk");
            spriteRenderer.flipX = false;
            transform.position = new Vector2(
                transform.position.x + speed * Time.deltaTime,
                transform.position.y
            );
        }
        else if (hDirection == -1f)
        {
            PlayAnimation("player_walk");
            spriteRenderer.flipX = true;
            transform.position = new Vector2(
                transform.position.x - speed * Time.deltaTime,
                transform.position.y
            );
        }
        else
        {
            PlayAnimation("player_idle");
        }

        if (vDirection == 1f) { }
        else if (vDirection == -1f) { }

        if (jumpPressed)
        {
            if (isGrounded && canJump)
            {
                rb2d.velocity = new Vector2(rb2d.velocity.x, 0);
                rb2d.AddForce(new Vector2(0, jumpForce), ForceMode2D.Impulse);
                canJump = false;
            }
        }
    }

    public bool GetIsGrounded()
    {
        return isGrounded;
    }

    private void PlayAnimation(string animacao)
    {
        if (!animationLocked)
        {
            if (animacao == "player_attack")
            {
                animationLocked = true;
            }

            if (emotion == "SAD")
                animationController.PlayAnimation(animacao + "_sad");
            else
                animationController.PlayAnimation(animacao);

            Invoke("UnlockAnimation", 0.5f);
        }
    }

    public void Hurt(int damage)
    {
        hp -= damage;

        spriteRenderer.color = Color.red;
        Invoke("ResetColor", 0.1f);

        if (hp < 1)
        {
            isAlive = false;
            PlayAnimation("player_death");
            Invoke("ResetGame", 3);
        }
    }

    private void ResetColor()
    {
        spriteRenderer.color = Color.white;
    }

    private void ResetGame()
    {
        gameManager.GetComponent<EmotionManager>().CloseServer();
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    private void UnlockAnimation(){
        animationLocked = false;
    }
}
