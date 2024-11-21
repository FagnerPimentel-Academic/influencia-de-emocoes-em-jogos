using System.Collections;
using System.Collections.Generic;
using System.Linq;
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
    private List<GameObject> enemyTarget = new List<GameObject>();

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
            if (!animationLocked)
            {
                Movement();
            }
            Attack();
        }

        if(Input.GetKeyDown(KeyCode.R))
            ResetGame();
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

    void OnTriggerEnter2D(Collider2D col)
    {
        if (col.CompareTag("Enemy"))
        {
            enemyTarget.Add(col.gameObject);
        }
    }

    void OnTriggerExit2D(Collider2D col)
    {
        if (col.CompareTag("Enemy"))
        {
            enemyTarget.Remove(col.gameObject);
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
        {
            PlaySmartAnimation("player_attack");

            if (enemyTarget.Count > 0)
            {
                foreach (GameObject enemy in enemyTarget)
                {
                    enemy.gameObject.GetComponent<EnemyController>().Hurt(1);
                }
            }
        }
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
            PlaySmartAnimation("player_walk");
            spriteRenderer.flipX = false;
            transform.position = new Vector2(
                transform.position.x + speed * Time.deltaTime,
                transform.position.y
            );
        }
        else if (hDirection == -1f)
        {
            PlaySmartAnimation("player_walk");
            spriteRenderer.flipX = true;
            transform.position = new Vector2(
                transform.position.x - speed * Time.deltaTime,
                transform.position.y
            );
        }
        else
        {
            PlaySmartAnimation("player_idle");
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

    private void PlaySmartAnimation(string animacao)
    {
        if (!animationLocked)
        {
            if (emotion == "SAD")
                animationController.PlayAnimation(animacao + "_sad");
            else
                animationController.PlayAnimation(animacao);

            if (animacao == "player_attack")
            {
                animationLocked = true;
                Invoke("UnlockAnimation", 0.250f);
            }
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
            PlaySmartAnimation("player_death");
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

    private void UnlockAnimation()
    {
        animationLocked = false;
    }
}
